from sqlalchemy.sql import expression
from sqlalchemy import Column, ForeignKey, Integer, Boolean

from app.models.base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    is_superuser = Column(Boolean, server_default=expression.false())


class UserRelatedMixin:
    user_id = Column(
        ForeignKey(f"{User.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
