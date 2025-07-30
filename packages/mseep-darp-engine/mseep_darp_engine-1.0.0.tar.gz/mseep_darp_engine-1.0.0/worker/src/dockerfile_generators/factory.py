from ..constants import BaseImage
from ..user_logger import UserLogger
from .base import DockerfileGenerator
from .python import PythonGenerator
from .typescript import TypeScriptGenerator
from .user_provided import UserDockerfileGenerator


async def get_dockerfile_generator(
    base_image: BaseImage,
    repo_folder: str,
    build_instructions: str | None,
    user_logger: UserLogger,
) -> DockerfileGenerator:
    if build_instructions:
        await user_logger.info(message="Build instructions found.")
        return UserDockerfileGenerator(
            base_image=base_image,
            repo_folder=repo_folder,
            build_instructions=build_instructions,
            user_logger=user_logger,
        )
    await user_logger.warning(
        message="No build instructions found. Attempting to generate from scratch."
    )
    if base_image == BaseImage.node_lts:
        return TypeScriptGenerator(
            base_image=base_image, repo_folder=repo_folder, user_logger=user_logger
        )
    else:
        return PythonGenerator(
            base_image=base_image, repo_folder=repo_folder, user_logger=user_logger
        )
