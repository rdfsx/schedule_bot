import enum
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.models.base import TimeBaseModel
from app.models.classroom import ClassRoomRelatedModel, ClassRoomModel
from app.models.classtime import ClassTimeRelatedModel, ClassTimeModel
from app.models.group import GroupRelatedModel, GroupModel
from app.models.lesson import LessonRelatedModel, LessonModel, LessonKind
from app.models.teacher import TeacherRelatedNullModel, TeacherModel


class Week(enum.Enum):
    monday = 'понедельник'
    tuesday = 'вторник'
    wednesday = 'среда'
    thursday = 'четверг'
    friday = 'пятница'
    saturday = 'суббота'
    sunday = 'воскресенье'

    @staticmethod
    def today():
        return Week[datetime.today().strftime('%A').lower()]

    def next(self):
        cls = self.__class__

        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            index = 0
        return members[index]


class UnderAboveWeek(enum.Enum):
    under, above, all = range(3)


class SourceTimetable(enum.Enum):
    DAYTIME, DISTANCE, MASTERS = range(3)


class TimetableModel(GroupRelatedModel,
                     LessonRelatedModel,
                     TeacherRelatedNullModel,
                     ClassTimeRelatedModel,
                     ClassRoomRelatedModel,
                     TimeBaseModel):
    id: int = sa.Column(sa.Integer, primary_key=True, unique=True)
    day_week: Week = sa.Column(sa.Enum(Week, native_enum=False), nullable=False)
    week: UnderAboveWeek = sa.Column(sa.Enum(UnderAboveWeek, native_enum=False), nullable=False)
    over_line: bool = sa.Column(sa.Boolean, default=False)
    below_line: bool = sa.Column(sa.Boolean, default=False)
    lesson_kind: LessonKind = sa.Column(sa.Enum(LessonKind, native_enum=False))
    source: SourceTimetable = sa.Column(sa.Enum(SourceTimetable, native_enum=False))

    group: GroupModel = relationship(GroupModel.__name__)
    lesson: LessonModel = relationship(LessonModel.__name__)
    teacher: TeacherModel = relationship(TeacherModel.__name__)
    classroom: ClassRoomModel = relationship(ClassRoomModel.__name__)
    classtime: ClassTimeModel = relationship(ClassTimeModel.__name__)
