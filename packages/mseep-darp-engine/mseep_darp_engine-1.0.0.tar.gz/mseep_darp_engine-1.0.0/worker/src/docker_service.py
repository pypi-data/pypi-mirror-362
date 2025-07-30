import subprocess
from pathlib import Path

from .constants import BaseImage
from .dockerfile_generators import DockerfileGenerator
from .dockerfile_generators import get_dockerfile_generator
from .errors import InvalidData
from .errors import ProcessingError
from .user_logger import UserLogger
from registry.src.database import Server
from registry.src.logger import logger
from registry.src.settings import settings


class DockerService:
    def __init__(
        self,
        docker_env: dict,
        repo_folder: str,
        server: Server,
        user_logger: UserLogger,
    ) -> None:
        self.docker_env = docker_env
        self.repo_folder = repo_folder
        self.server = server
        self.image_name = f"hipasus/{self.server.name}"
        self.container_name = f"darp_server_{server.id}"
        self.user_logger = user_logger

    async def clone_repo(self) -> None:
        await self._execute(["git", "clone", self.server.repo_url, self.repo_folder])

    def dockerfile_exists(self) -> bool:
        path = Path(f"{self.repo_folder}/Dockerfile")
        return path.exists()

    async def generate_dockerfile(self) -> None:
        if not self.server.base_image:
            await self.user_logger.error(message="No base image provided.")
            raise InvalidData
        generator: DockerfileGenerator = await get_dockerfile_generator(
            repo_folder=self.repo_folder,
            base_image=BaseImage(self.server.base_image),
            build_instructions=self.server.build_instructions,
            user_logger=self.user_logger,
        )
        try:
            logs = await generator.generate_dockerfile()
            await self.user_logger.info(message=f"Generated Dockerfile:\n{logs}")
            logger.info(logs)
        except ProcessingError as error:
            await self.user_logger.error(
                message=f"Error generating Dockerfile: {error.message or ''}"
            )
            raise

    async def build_image(self) -> None:
        command = [
            "docker",
            "build",
            "-t",
            self.image_name,
            "-f",
            f"{self.repo_folder}/Dockerfile",
            self.repo_folder,
        ]
        await self._execute(command)

    async def push_image(self) -> None:
        docker_push_command = (
            f"docker login -u {settings.dockerhub_login} -p {settings.dockerhub_password} && docker image push {self.image_name}",
        )
        await self.user_logger.info("Pushing image...")
        result = subprocess.run(docker_push_command, shell=True)
        if result.returncode != 0:
            await self.user_logger.error(message="Docker push failed")
            logger.error("docker push failed")
            raise ProcessingError

    async def run_container(self) -> None:
        subprocess.run(
            ["docker", "rm", self.container_name, "--force"], env=self.docker_env
        )
        run_command = [
            "docker",
            "run",
            "--network",
            settings.deployment_network,
            "-d",
            "--restart",
            "always",
            "--pull",
            "always",
            "--name",
            self.container_name,
            self.image_name,
        ]
        if self.server.command:
            run_command.extend(["sh", "-c", self.server.command])
        await self._execute(command=run_command, env=self.docker_env)

    async def _execute(self, command: list[str], env: dict | None = None) -> None:
        command_str = " ".join(command)
        logger.info(f"{command_str=}")
        await self.user_logger.command_start(command=command_str)
        arguments: dict = dict(
            args=command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if env:
            arguments["env"] = env
        result = subprocess.run(**arguments)
        output = result.stdout.decode() if result.stdout else ""  # noqa
        if result.returncode != 0:
            await self.user_logger.command_result(output=output, success=False)
            logger.error(f"{' '.join(command[:2])} failed")
            raise ProcessingError
        await self.user_logger.command_result(output=output, success=True)
