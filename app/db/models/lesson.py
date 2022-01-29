import enum
import typing
from dataclasses import dataclass

import sqlalchemy as sa
from sqlalchemy.orm import declared_attr

from app.constants.convert import lessons_emoji
from app.db.models.base import TimeBaseModel
from app.db.models.timetable import Week


class LessonKind(enum.Enum):
    LEC = 'лекц.'
    PRAC = 'практ.'
    LAB = 'лаб.'

    def __str__(self) -> str:
        return f"<i>({self.value})</i>"


@dataclass
class Lesson:
    number: typing.Literal[1, 2, 3, 4, 5, 6, 7, 8]
    classroom: str
    classtime: str
    group: str
    lesson: str
    teacher: str
    lesson_kind: LessonKind
    day_week: Week

    def __str__(self):
        return f"{lessons_emoji[self.number]}" \
               f"<i>{self.lesson_kind.value}</i> " \
               f"{self.lesson} " \
               f"{self.classroom} " \
               f"<code>{self.teacher}</code> " \
               f"<i><u>{self.classtime}</u></i>"


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
