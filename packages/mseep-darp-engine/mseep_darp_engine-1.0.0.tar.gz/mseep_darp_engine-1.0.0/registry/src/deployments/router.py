from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from .schemas import DeploymentCreate
from .schemas import ServerLogsSchema
from .schemas import UserId
from .service import DeploymentService
from registry.src.database import Server
from registry.src.database import ServerLogs
from registry.src.servers.schemas import ServerRead

router = APIRouter(prefix="/deployments")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ServerRead)
async def create_server(
    data: DeploymentCreate,
    service: DeploymentService = Depends(DeploymentService.get_new_instance),
) -> Server:
    server = await service.create_server(data)
    return server


@router.get("/{server_id}/logs", response_model=ServerLogsSchema)
async def get_logs(
    server_id: int,
    current_user_id: str,
    service: DeploymentService = Depends(DeploymentService.get_new_instance),
) -> ServerLogs:
    logs = await service.get_logs(server_id=server_id, current_user_id=current_user_id)
    return logs


@router.post("/{server_id}/stop", status_code=status.HTTP_202_ACCEPTED)
async def stop_server(
    server_id: int,
    user_id: UserId,
    service: DeploymentService = Depends(DeploymentService.get_new_instance),
) -> None:
    await service.stop_server(
        server_id=server_id, current_user_id=user_id.current_user_id
    )


@router.post("/{server_id}/start", status_code=status.HTTP_202_ACCEPTED)
async def start_server(
    server_id: int,
    user_id: UserId,
    service: DeploymentService = Depends(DeploymentService.get_new_instance),
) -> None:
    await service.start_server(
        server_id=server_id, current_user_id=user_id.current_user_id
    )
