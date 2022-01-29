import sqlalchemy as sa
from sqlalchemy.orm import declared_attr, relationship
from sqlalchemy.sql import expression

from app.db.models.base import TimeBaseModel
from app.db.models.group import GroupRelatedModel, GroupModel


class UserModel(GroupRelatedModel, TimeBaseModel):
    id: int = sa.Column(sa.BigInteger, primary_key=True, index=True, unique=True)
    is_superuser: bool = sa.Column(sa.Boolean, server_default=expression.false())

    group: GroupModel = relationship(GroupModel.__name__)


class UserRelatedModel:
    __abstract__ = True

    @declared_attr
    def user_id(self):
        return sa.Column(
            sa.ForeignKey(f"{UserModel.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False,
        )
