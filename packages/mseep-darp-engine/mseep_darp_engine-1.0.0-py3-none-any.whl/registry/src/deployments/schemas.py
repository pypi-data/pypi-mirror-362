from datetime import datetime
from typing import Annotated

from pydantic import Field
from pydantic import field_serializer
from pydantic import HttpUrl

from registry.src.base_schema import BaseSchema
from registry.src.servers.schemas import server_name_regex_pattern
from registry.src.types import HostType
from registry.src.types import ServerStatus
from worker.src.constants import BaseImage
from worker.src.schemas import LogMessage


class ServerLogsSchema(BaseSchema):
    server_id: int
    deployment_logs: list[LogMessage]
    created_at: datetime
    updated_at: datetime


class DeploymentCreateData(BaseSchema):
    name: Annotated[str, Field(max_length=30, pattern=server_name_regex_pattern)]
    title: str = Field(max_length=30)
    description: str
    repo_url: HttpUrl
    command: str | None = None
    logo: str | None = None
    base_image: BaseImage | None = None
    build_instructions: str | None = None
    host_type: HostType = HostType.internal
    status: ServerStatus = ServerStatus.in_processing

    @field_serializer("repo_url")
    def serialize_url(self, repo_url: HttpUrl) -> str:
        return str(repo_url)


class DeploymentCreate(BaseSchema):
    current_user_id: str
    data: DeploymentCreateData


class UserId(BaseSchema):
    current_user_id: str
