from pathlib import Path
from typing import override

from ...errors import DependenciesError
from ..base import DockerfileGenerator


class TypeScriptGenerator(DockerfileGenerator):
    @override
    async def _dependencies_installation(self) -> None:
        repo_path = Path(self.repo_folder)
        package_json = self._find_file(repo_path, "package.json")
        if not package_json:
            await self.user_logger.error(message="Error: no package.json found")
            raise DependenciesError("No package.json found")
        await self.user_logger.info(message="package.json found. Adding to Dockerfile")
        package_json_folder = self._relative_path(package_json.parent.absolute())
        lines = [
            f"COPY {package_json_folder}/package*.json ./",
        ]
        ts_config = self._find_file(repo_path, "tsconfig.json")
        if ts_config:
            await self.user_logger.info(
                message="tsconfig.json found. Adding to Dockerfile"
            )
            lines.append(f"COPY {self._relative_path(ts_config.absolute())} ./")
        lines.append("RUN npm install --ignore-scripts")
        self._add_to_file(lines)

    @override
    async def _code_setup(self) -> None:
        lines = [
            "COPY ./ ./",
            "RUN npm run build",
        ]
        self._add_to_file(lines)
