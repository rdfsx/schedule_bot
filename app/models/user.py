from sqlalchemy import Column, BigInteger, Boolean, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from app.models.base import TimedBaseModel
from app.models.group import GroupRelatedModel


class UserModel(GroupRelatedModel, TimedBaseModel):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    is_superuser = Column(Boolean, server_default=expression.false())
    group = relationship("GroupModel")


class UserRelatedModel:
    __abstract__ = True

    user_id = Column(
        ForeignKey(f"{UserModel.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
