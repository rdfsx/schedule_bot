from sqlalchemy import Column, Integer, Enum, SmallInteger
from sqlalchemy.orm import relationship

from app.enums.lessons import LessonKind
from app.enums.week import Week, UnderAboveWeek
from app.models.base import TimedBaseModel
from app.models.group import GroupRelatedModel, GroupModel
from app.models.lesson import LessonRelatedModel, LessonModel
from app.models.teacher import TeacherRelatedModelNull, TeacherModel


class TimetableModel(GroupRelatedModel,
                     LessonRelatedModel,
                     TeacherRelatedNullModel,
                     ClassTimeRelatedModel,
                     ClassRoomRelatedModel,
                     TimeBaseModel):
    id: int = Column(Integer, primary_key=True, unique=True)
    day_week: Week = Column(Enum(Week, native_enum=False), nullable=False)
    week: UnderAboveWeek = Column(Enum(UnderAboveWeek, native_enum=False), nullable=False)
    over_line: bool = Column(Boolean, default=False)
    below_line: bool = Column(Boolean, default=False)
    lesson_kind: LessonKind = Column(Enum(LessonKind, native_enum=False))
    source: SourceTimetable = Column(Enum(SourceTimetable, native_enum=False))

    group: GroupModel = relationship(GroupModel.__name__)
    lesson: LessonModel = relationship(LessonModel.__name__)
    teacher: TeacherModel = relationship(TeacherModel.__name__)
    classroom: ClassRoomModel = relationship(ClassRoomModel.__name__)
    classtime: ClassTimeModel = relationship(ClassTimeModel.__name__)
