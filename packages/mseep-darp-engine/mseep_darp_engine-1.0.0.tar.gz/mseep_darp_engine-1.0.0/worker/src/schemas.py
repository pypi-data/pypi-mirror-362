from datetime import datetime
from enum import auto
from enum import StrEnum

from pydantic import Field
from pydantic import field_serializer

from registry.src.base_schema import BaseSchema
from registry.src.types import TaskType


class Task(BaseSchema):
    task_type: TaskType
    server_id: int


class LogLevel(StrEnum):
    info = auto()
    warning = auto()
    error = auto()


class LoggingEvent(StrEnum):
    command_start = auto()
    command_result = auto()
    general_message = auto()


class CommandStart(BaseSchema):
    command: str


class CommandResult(BaseSchema):
    output: str
    success: bool


class GeneralLogMessage(BaseSchema):
    log_level: LogLevel
    message: str


class LogMessage(BaseSchema):
    event_type: LoggingEvent
    data: CommandStart | CommandResult | GeneralLogMessage
    timestamp: datetime = Field(default_factory=datetime.now)

    @field_serializer("timestamp")
    def serialize_datetime(self, value: datetime, _info) -> str:
        return value.isoformat()
