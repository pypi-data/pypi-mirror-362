import asyncio
import os
import tempfile
from logging import Logger

from .docker_service import DockerService
from .user_logger import UserLogger
from common.notifications.client import NotificationsClient
from registry.src.database import Server
from registry.src.errors import InvalidData
from registry.src.servers.repository import ServerRepository
from registry.src.servers.schemas import ServerUpdateData
from registry.src.servers.schemas import Tool
from registry.src.servers.service import ServerService
from registry.src.settings import settings
from registry.src.types import ServerStatus
from registry.src.types import ServerTransportProtocol
from worker.src.errors import ProcessingError


class WorkerDeploymentService:
    def __init__(self, repo: ServerRepository, logger: Logger):
        self.repo = repo
        self.logger = logger
        self.docker_env = dict(**os.environ)
        self.docker_env["DOCKER_HOST"] = settings.deployment_server
        self.notifications_client = NotificationsClient()

    async def deploy_server(self, server_id: int) -> None:
        server = await self.repo.get_server(id=server_id)
        if not server:
            raise ProcessingError
        with tempfile.TemporaryDirectory(
            prefix=f"server_{server.id}", dir="/tmp"
        ) as repo_folder:
            user_logger = UserLogger(session=self.repo.session, server_id=server_id)
            await user_logger.clear_logs()
            service = DockerService(
                docker_env=self.docker_env,
                repo_folder=repo_folder,
                server=server,
                user_logger=user_logger,
            )
            server_url = f"http://{service.container_name}/sse"
            try:
                await self._deploy_repo(service=service)
                tools = await self._get_tools(
                    server=server, service=service, server_url=server_url
                )
            except Exception:
                await self._handle_deploy_failure(server)
                raise
        await user_logger.info("Deployment complete.")
        await self._handle_deploy_success(
            tools=tools,
            server=server,
            url=server_url,
            transport_protocol=ServerTransportProtocol.SSE,
        )

    async def _deploy_repo(self, service: DockerService) -> None:
        await service.clone_repo()
        if not service.dockerfile_exists():
            self.logger.info(f"No Dockerfile in repo: {service.server.repo_url}")
            await self._ensure_command(service)
            await service.user_logger.info(
                message="No Dockerfile found in the project. Attempting to generate..."
            )
            await service.generate_dockerfile()
        await service.build_image()
        await service.push_image()
        await service.run_container()

    async def _handle_deploy_failure(self, server: Server) -> None:
        await self.repo.update_server(
            id=server.id,
            data=ServerUpdateData(),
            status=ServerStatus.processing_failed,
        )

        await self.notifications_client.notify_deploy_failed(
            user_id=server.creator_id,
            server_name=server.name,
        )

    async def _handle_deploy_success(
        self,
        tools: list[Tool],
        server: Server,
        url: str,
        transport_protocol: ServerTransportProtocol,
    ) -> None:
        await self.repo.update_server(
            id=server.id,
            tools=tools,
            data=ServerUpdateData(url=url),
            status=ServerStatus.active,
            transport_protocol=transport_protocol,
        )

        await self.notifications_client.notify_deploy_successful(
            user_id=server.creator_id,
            server_name=server.name,
        )

    async def _get_tools(
        self, server: Server, service: DockerService, server_url: str
    ) -> list[Tool]:
        for i in range(settings.tool_retry_count):
            tools = await self._fetch_tools(
                server=server, server_url=server_url, service=service
            )
            if tools:
                return tools
        await service.user_logger.error("Error getting tools from server")
        raise ProcessingError

    async def _fetch_tools(
        self, server: Server, server_url: str, service: DockerService
    ) -> list[Tool] | None:
        try:
            await service.user_logger.info(
                f"Waiting {settings.tool_wait_interval} seconds for server to start up"
            )
            await asyncio.sleep(settings.tool_wait_interval)
            tools = await ServerService.get_tools(
                server_url=server_url, server_name=server.name
            )
            await service.user_logger.info(
                "Successfully got a list of tools from server"
            )
            return tools
        except InvalidData:
            await service.user_logger.warning("Failed to connect to server")
            return None

    @staticmethod
    async def _ensure_command(service: DockerService):
        if not service.server.command:
            await service.user_logger.error(
                "Command must not be empty if project does not have a Dockerfile"
            )
            raise ProcessingError
