from pathlib import Path
from typing import override

from ...errors import DependenciesError
from ..base import DockerfileGenerator


class PythonGenerator(DockerfileGenerator):
    @override
    async def _dependencies_installation(self) -> None:
        repo_path = Path(self.repo_folder)
        await self._install_node()
        uv_file = self._find_file(repo_path, "uv.lock")
        pyproject_file = self._find_file(repo_path, "pyproject.toml")
        readme_file = self._find_file(repo_path, "README.md")
        if pyproject_file and readme_file:
            await self.user_logger.info(
                message="pyproject.toml found. Installing dependencies with pip"
            )
            self._pip_dependencies(pyproject=pyproject_file, readme_file=readme_file)
            return
        requirements_file = self._find_file(repo_path, "requirements.txt")
        if requirements_file:
            await self.user_logger.info(
                message="requirements.txt found. Installing dependencies with legacy pip method"
            )
            self._legacy_pip_dependencies(requirements_file)
            return
        if uv_file and pyproject_file and readme_file:
            await self.user_logger.info(
                message="uv.lock found. Installing dependencies with uv"
            )
            self._uv_dependencies(
                uv_file=uv_file, pyproject=pyproject_file, readme_file=readme_file
            )
            return
        raise DependenciesError("No supported dependencies installation method found")

    @override
    async def _code_setup(self) -> None:
        lines = [
            "COPY ./ ./",
        ]
        self._add_to_file(lines)

    async def _install_node(self) -> None:
        await self.user_logger.info(message="Adding nodejs for supergateway")
        lines = [
            "RUN apt update && apt install -y nodejs npm",
        ]
        self._add_to_file(lines)

    def _legacy_pip_dependencies(self, requirements: Path) -> None:
        lines = [
            f"COPY {self._relative_path(requirements.absolute())} ./requirements.txt",
            "RUN pip install -r requirements.txt",
        ]
        self._add_to_file(lines)

    def _pip_dependencies(self, pyproject: Path, readme_file: Path) -> None:
        lines = [
            f"COPY {self._relative_path(pyproject.absolute())} ./pyproject.toml",
            f"COPY {self._relative_path(readme_file.absolute())} ./README.md",
            "RUN pip install .",
        ]
        self._add_to_file(lines)

    def _uv_dependencies(
        self, uv_file: Path, pyproject: Path, readme_file: Path
    ) -> None:
        lines = [
            "COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/",
            f"COPY {self._relative_path(uv_file.absolute())} ./uv.lock",
            f"COPY {self._relative_path(pyproject.absolute())} ./pyproject.toml",
            f"COPY {self._relative_path(readme_file.absolute())} ./README.md",
            "RUN uv pip install . --system",
        ]
        self._add_to_file(lines)
