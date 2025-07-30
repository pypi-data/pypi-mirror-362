from enum import auto
from enum import StrEnum


class HostType(StrEnum):
    internal = auto()
    external = auto()


class ServerStatus(StrEnum):
    active = auto()
    inactive = auto()
    in_processing = auto()
    stopped = auto()
    processing_failed = auto()


class TaskType(StrEnum):
    deploy = auto()
    start = auto()
    stop = auto()


class ServerTransportProtocol(StrEnum):
    SSE = "SSE"
    STREAMABLE_HTTP = "STREAMABLE_HTTP"


class RoutingMode(StrEnum):
    auto = "auto"
    deepresearch = "deepresearch"
