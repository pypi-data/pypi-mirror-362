from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from ...database import models
from ...types import HostType
from ...types import ServerTransportProtocol
from .base import Base
from .mixins import HasCreatedAt
from .mixins import HasUpdatedAt
from registry.src.types import ServerStatus


class Server(HasCreatedAt, HasUpdatedAt, Base):
    __tablename__ = "server"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(), nullable=False)
    url: Mapped[str | None] = mapped_column(String(), nullable=True, unique=True)
    name: Mapped[str] = mapped_column(String(), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(), nullable=False)
    logo: Mapped[str | None] = mapped_column(String(), nullable=True)
    host_type: Mapped[HostType] = mapped_column(String(), nullable=False)
    creator_id: Mapped[str | None] = mapped_column(String(), nullable=True)
    repo_url: Mapped[str | None] = mapped_column(String(), nullable=True, unique=True)
    command: Mapped[str | None] = mapped_column(String(), nullable=True)
    base_image: Mapped[str | None] = mapped_column(String(), nullable=True)
    transport_protocol: Mapped[ServerTransportProtocol | None] = mapped_column(
        String(),
        nullable=True,
    )
    build_instructions: Mapped[str | None] = mapped_column(String(), nullable=True)
    tools: Mapped[list["models.tool.Tool"]] = relationship(
        back_populates="server", cascade="all, delete-orphan"
    )
    status: Mapped[ServerStatus] = mapped_column(
        String(), nullable=False, default=ServerStatus.active
    )
