from typing import override
from uuid import uuid4

from ..user_logger import UserLogger
from .base import DockerfileGenerator
from worker.src.constants import BaseImage


class UserDockerfileGenerator(DockerfileGenerator):
    def __init__(
        self,
        base_image: BaseImage,
        repo_folder: str,
        user_logger: UserLogger,
        build_instructions: str,
    ) -> None:
        self.build_instructions = build_instructions
        super().__init__(
            base_image=base_image, repo_folder=repo_folder, user_logger=user_logger
        )

    @override
    async def generate_dockerfile(self) -> str:
        await self._image_setup()
        await self._code_setup()
        return self._save_dockerfile()

    @override
    async def _code_setup(self) -> None:
        heredoc_identifier = str(uuid4()).replace("-", "")
        lines = [
            "COPY ./ ./",
            f"RUN <<{heredoc_identifier}",
            self.build_instructions,
            heredoc_identifier,
        ]
        self._add_to_file(lines)
