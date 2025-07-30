from httpx import AsyncClient

from common.notifications.enums import NotificationEvent
from common.notifications.exceptions import NotificationsServiceError

DEFAULT_NOTIFICATIONS_CLIENT_URI: str = "http://mailing_api:8000"


class NotificationsClient:
    def __init__(self, base_url: str | None = None) -> None:
        if base_url is None:
            base_url = DEFAULT_NOTIFICATIONS_CLIENT_URI

        self._client: AsyncClient = AsyncClient(base_url=base_url)

    async def _notify(
        self,
        user_id: str,
        template: NotificationEvent,
        data: dict,
    ) -> None:
        response = await self._client.post(
            f"/v1/emails/{template.value}",
            json=dict(user_id=user_id, **data),
        )

        if response.status_code != 200:
            raise NotificationsServiceError(f"Failed to send email: {response.text}")

    async def send_server_down_alert(
        self,
        user_id: str,
        server_name: str,
        server_logs: str | None = None,
    ):
        await self._notify(
            user_id,
            NotificationEvent.server_healthcheck_failed,
            data={
                "server_name": server_name,
                "server_logs": server_logs,
            },
        )

    async def notify_deploy_failed(self, user_id: str, server_name: str) -> None:
        await self._notify(
            user_id,
            NotificationEvent.deploy_failed,
            data={
                "server_name": server_name,
            },
        )

    async def notify_deploy_successful(self, user_id: str, server_name: str) -> None:
        await self._notify(
            user_id,
            NotificationEvent.deploy_successful,
            data={
                "server_name": server_name,
            },
        )
