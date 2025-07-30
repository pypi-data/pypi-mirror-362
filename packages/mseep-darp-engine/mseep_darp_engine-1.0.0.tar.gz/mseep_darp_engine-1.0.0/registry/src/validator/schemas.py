from enum import Enum

from pydantic import BaseModel
from pydantic import Field
from pydantic import RootModel

from registry.src.servers.schemas import ServerCreate
from registry.src.servers.schemas import Tool


class SSLAuthorityLevel(Enum):
    NO_CERTIFICATE = 0
    INVALID_CERTIFICATE = 1
    SELF_SIGNED_CERTIFICATE = 2
    CERTIFICATE_OK = 3
    EXTENDED_CERTIFICATE = 4


class ServerNeedsSensitiveDataResponse(BaseModel):
    reasoning: list[str] = Field(
        ...,
        description="For each argument of each tool describe if you can send sensitive data to this argument, and what kind of it",
    )
    server_needs_sensitive_data: bool


class ServerWithTools(ServerCreate):
    tools: list[Tool]


class ValidationResult(BaseModel):
    server_requires_sensitive_data: bool = False
    authority_level: SSLAuthorityLevel = SSLAuthorityLevel.NO_CERTIFICATE


Tools = RootModel[list[Tool]]
