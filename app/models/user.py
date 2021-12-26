from sqlalchemy import Column, BigInteger, Boolean, ForeignKey, SmallInteger
from sqlalchemy.sql import expression

from app.models.base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    is_superuser = Column(Boolean, server_default=expression.false())
    subgroup = Column(SmallInteger)


class UserRelatedMixin:
    __abstract__ = True

    user_id = Column(
        ForeignKey(f"{User.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
