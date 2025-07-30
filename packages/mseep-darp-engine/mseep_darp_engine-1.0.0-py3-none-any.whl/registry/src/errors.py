from fastapi import HTTPException
from fastapi import status


class FastApiError(HTTPException):

    def __init__(self, message: str, **kwargs) -> None:
        self.detail = {"message": message, **kwargs}


class InvalidServerNameError(FastApiError):
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, name: str) -> None:
        message = "Name must have only letters, digits, underscore. Name must not start with digits."
        super().__init__(message=message, name=name)


class ServerAlreadyExistsError(FastApiError):
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, dict_servers: list[dict]) -> None:
        servers_str = ", ".join(server["name"] for server in dict_servers)
        message = f"Server already exists: {servers_str}"
        super().__init__(message=message, servers=dict_servers)


class ServersNotFoundError(FastApiError):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, ids: list[int]) -> None:
        super().__init__(message=f"Server(s) not found: {ids}", ids=ids)


class NotAllowedError(FastApiError):
    status_code = status.HTTP_403_FORBIDDEN


class InvalidData(FastApiError):
    status_code = status.HTTP_400_BAD_REQUEST


class RemoteServerError(FastApiError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
