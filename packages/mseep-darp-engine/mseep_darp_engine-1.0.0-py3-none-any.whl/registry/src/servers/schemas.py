from datetime import datetime
from typing import Annotated
from typing import Any

from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_serializer

from registry.src.base_schema import BaseSchema
from registry.src.types import HostType
from registry.src.types import ServerStatus
from registry.src.types import ServerTransportProtocol
from worker.src.constants import BaseImage


tool_name_regex = "^[a-zA-Z0-9_-]{1,64}$"
server_name_regex_pattern = "^[a-z0-9]+(_[a-z0-9]+)*$"


class Tool(BaseSchema):
    model_config = ConfigDict(populate_by_name=True, **BaseSchema.model_config)
    name: str = Field(pattern=tool_name_regex)
    alias: str = Field(pattern=tool_name_regex)
    description: str
    input_schema: dict[str, Any] = Field(validation_alias="inputSchema")


class ServerCreateData(BaseSchema):
    name: Annotated[str, Field(pattern=server_name_regex_pattern, max_length=30)]
    title: str = Field(max_length=30)
    description: str
    url: str
    logo: str | None = None
    host_type: HostType = HostType.external


class ServerCreate(BaseSchema):
    data: ServerCreateData
    current_user_id: str | None = None


class ServerRead(BaseSchema):
    title: str
    id: int
    status: ServerStatus
    name: str
    creator_id: str | None
    description: str
    repo_url: str | None
    url: str | None
    command: str | None
    logo: str | None
    host_type: HostType
    base_image: BaseImage | None = None
    build_instructions: str | None = None
    transport_protocol: ServerTransportProtocol | None
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, value: datetime, _info) -> str:
        return value.isoformat()


class ServerWithTools(ServerRead):
    tools: list[Tool]


class ServerUpdateData(BaseSchema):
    title: str | None = Field(max_length=30, default=None)
    name: Annotated[
        str | None, Field(pattern=server_name_regex_pattern, max_length=30)
    ] = None
    description: str | None = None
    url: str | None = None
    logo: str | None = None


class DeploymentUpdateData(BaseSchema):
    command: str | None = None
    repo_url: str | None = None
    base_image: BaseImage | None = None
    build_instructions: str | None = None


class ServerUpdate(BaseSchema):
    data: ServerUpdateData
    deployment_data: DeploymentUpdateData
    current_user_id: str | None = None


class MCP(BaseSchema):
    name: str
    description: str
    endpoint: str = Field(validation_alias="url")
    logo: str | None = None


class MCPJson(BaseSchema):
    version: str = "1.0"
    servers: list[MCP]
