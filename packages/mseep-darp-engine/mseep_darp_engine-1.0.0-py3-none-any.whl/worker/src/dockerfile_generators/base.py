from pathlib import Path

from ..constants import BaseImage
from ..user_logger import UserLogger


class DockerfileGenerator:
    def __init__(
        self, base_image: BaseImage, repo_folder: str, user_logger: UserLogger
    ):
        self.base_image = base_image
        self.lines: list[str] = []
        self.repo_folder = repo_folder
        self.user_logger = user_logger

    async def generate_dockerfile(self) -> str:
        await self._image_setup()
        await self._dependencies_installation()
        await self._code_setup()
        return self._save_dockerfile()

    async def _image_setup(self) -> None:
        lines = [
            f"FROM {self.base_image.value}",
            "WORKDIR /workspace",
        ]
        self._add_to_file(lines)

    async def _dependencies_installation(self) -> None:
        raise NotImplementedError

    async def _code_setup(self) -> None:
        raise NotImplementedError

    def _add_to_file(self, lines: list[str]) -> None:
        self.lines.extend(lines)

    @staticmethod
    def _find_file(repo_folder: Path, file: str) -> Path | None:
        files = repo_folder.rglob(file)
        try:
            return next(files)
        except StopIteration:
            return None

    def _save_dockerfile(self) -> str:
        dockerfile_text = "\n".join(self.lines)
        with open(f"{self.repo_folder}/Dockerfile", "w") as dockerfile:
            dockerfile.write(dockerfile_text)
        return dockerfile_text

    def _relative_path(self, path: Path) -> str:
        str_path = str(path)
        if str_path.startswith(self.repo_folder):
            return "." + str(str_path[len(self.repo_folder) :])
        return str_path
