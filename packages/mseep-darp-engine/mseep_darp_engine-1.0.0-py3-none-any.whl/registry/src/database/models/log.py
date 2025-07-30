from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base
from .mixins import HasCreatedAt
from .mixins import HasServerId
from .mixins import HasUpdatedAt


class ServerLogs(HasCreatedAt, HasUpdatedAt, HasServerId, Base):
    __tablename__ = "server_logs"

    deployment_logs: Mapped[list[dict]] = mapped_column(
        JSONB(), nullable=False, server_default="'[]'::jsonb"
    )
