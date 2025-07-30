from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import declarative_mixin
from sqlalchemy.orm import declared_attr


@declarative_mixin
class HasServerId:
    @declared_attr
    def server_id(cls):
        return Column(
            Integer,
            ForeignKey("server.id", ondelete="CASCADE"),
            nullable=False,
            primary_key=True,
        )
