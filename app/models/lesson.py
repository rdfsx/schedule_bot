import enum

import sqlalchemy as sa
from sqlalchemy.orm import declared_attr

from app.models.base import TimeBaseModel


class LessonKind(enum.Enum):
    LEC = 'лекц.'
    PRAC = 'практ.'
    LAB = 'лаб.'

    def __str__(self) -> str:
        return f"<i>({self.value})</i>"


class LessonModel(TimeBaseModel):
    id: int = sa.Column(sa.Integer, primary_key=True, index=True, unique=True)
    name: str = sa.Column(sa.String(500), nullable=False, unique=True)


class LessonRelatedModel:
    __abstract__ = True

    @declared_attr
    def lesson_id(self):
        return sa.Column(
            sa.ForeignKey(f"{LessonModel.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'),
            nullable=False,
        )
