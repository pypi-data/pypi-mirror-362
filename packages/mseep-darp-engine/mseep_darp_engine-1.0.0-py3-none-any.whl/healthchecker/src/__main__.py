import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from common.notifications.client import NotificationsClient
from healthchecker.src.checker import HealthChecker
from registry.src.database.session import get_unmanaged_session
from registry.src.servers.repository import ServerRepository
from registry.src.settings import settings

logger: logging.Logger = logging.getLogger("Healthchecker")


def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting healthchecker")
    logger.info(
        "Healthchecker will run every %d seconds", settings.healthcheck_running_interval
    )


async def perform_healthcheck_step() -> None:
    logger.info("Running health-checks")
    session: AsyncSession = await get_unmanaged_session()
    repo: ServerRepository = ServerRepository(session)
    notifications_client: NotificationsClient = NotificationsClient()
    healthchecker: HealthChecker = HealthChecker(
        session=session,
        servers_repo=repo,
        notifications_client=notifications_client,
    )

    try:
        await healthchecker.run_once()
    except Exception as error:
        logger.error("Error in healthchecker", exc_info=error)

    logger.info("Health-checks finished")
    logger.info("Sleeping for %d seconds", settings.healthcheck_running_interval)

    await session.commit()
    await session.close()


async def main() -> None:
    setup_logging()

    while True:
        await perform_healthcheck_step()
        await asyncio.sleep(settings.healthcheck_running_interval)


if __name__ == "__main__":
    asyncio.run(main())
