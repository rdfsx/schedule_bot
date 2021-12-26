from sqlalchemy import Column, Integer, Enum, SmallInteger
from sqlalchemy.orm import relationship

from app.enums.lessons import LessonKind
from app.enums.week import Week, UnderAboveWeek
from app.models.base import TimedBaseModel
from app.models.group import GroupRelatedModel, GroupModel
from app.models.lesson import LessonRelatedModel, LessonModel
from app.models.teacher import TeacherRelatedModelNull, TeacherModel


class Timetable(GroupRelatedModel,
                LessonRelatedModel,
                TeacherRelatedModelNull,
                TimedBaseModel):
    __tablename__ = 'timetable'

    id = Column(Integer, primary_key=True, unique=True)
    day_week = Column(Enum(Week, native_enum=False), nullable=False)
    lesson_num = Column(SmallInteger)
    week = Column(Enum(UnderAboveWeek, native_enum=False), nullable=False)
    lesson_kind = Column(Enum(LessonKind, native_enum=False))
    source = ...  # TODO: поле для источника информации

    group = relationship(GroupModel.__tablename__)
    lesson = relationship(LessonModel.__tablename__)
    teacher = relationship(TeacherModel.__tablename__)
