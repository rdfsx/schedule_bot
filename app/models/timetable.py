from sqlalchemy import Column, Integer, Enum, SmallInteger

from app.enums.lessons import LessonKind
from app.enums.week import Week, UnderAboveWeek
from app.models.base import TimedBaseModel
from app.models.group import GroupRelatedModel
from app.models.lesson import LessonRelatedModel
from app.models.teacher import TeacherRelatedModelNull


class Timetable(GroupRelatedModel,
                LessonRelatedModel,
                TeacherRelatedModelNull,
                TimedBaseModel):
    __tablename__ = 'timetables'

    id = Column(Integer, primary_key=True, unique=True)
    day_week = Column(Enum(Week, native_enum=False), nullable=False)
    lesson_num = Column(SmallInteger)
    week = Column(Enum(UnderAboveWeek, native_enum=False), nullable=False)
    subgroup = Column(SmallInteger, nullable=False)
    lesson_kind = Column(Enum(LessonKind, native_enum=False))
    source = ...  # TODO: поле для источника информации
