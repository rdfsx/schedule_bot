import enum
import typing

import sqlalchemy as sa
from sqlalchemy.orm import declared_attr

from app.db.models.base import TimeBaseModel


class Fuckult(enum.Enum):
    FAIS = 1
    GEF = 2
    EF = 3
    MTF = 4
    MSF = 5
    UNKNOWN = 6


class GroupModel(TimeBaseModel):
    id: int = sa.Column(sa.Integer, primary_key=True, index=True, unique=True)
    name: str = sa.Column(sa.String(20), nullable=False)
    subgroups: int = sa.Column(sa.SmallInteger, nullable=False)

    __table_args__ = (
        sa.UniqueConstraint(name, typing.cast(sa.Column, subgroups)),
    )


class GroupRelatedModel:
    __abstract__ = True

    @declared_attr
    def group_id(self):
        return sa.Column(
            sa.ForeignKey(f"{GroupModel.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'),
        )
