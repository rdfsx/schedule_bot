from sqlalchemy import Column, String, sql, Integer, ForeignKey, SmallInteger, Index
from sqlalchemy import Enum

from app.enums.lessons import LessonKind
from app.enums.week import UnderAboveWeek, Week
from app.utils.db_api.db_gino import TimedBaseModel, BaseModel
from app.utils.db_api.schemas.group import GroupsRelatedModel
from app.utils.db_api.schemas.teacher import TeacherRelatedModelNull


class Lessons(TimedBaseModel):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    lesson = Column(String(300), nullable=False, unique=True)

    query: sql.Select


class LessonsRelatedModel(BaseModel):
    __abstract__ = True
    lesson_id = Column(ForeignKey(f"{Lessons.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'),
                       nullable=False)


class Timetable(GroupsRelatedModel, LessonsRelatedModel, TeacherRelatedModelNull, TimedBaseModel):
    __tablename__ = 'timetables'

    id = Column(Integer, primary_key=True, unique=True)
    day_week = Column(Enum(Week, native_enum=False), nullable=False)
    lesson_time = Column(String(20))
    lesson_num = Column(SmallInteger)
    week = Column(Enum(UnderAboveWeek, native_enum=False), nullable=False)
    subgroup = Column(SmallInteger, nullable=False)
    lesson_kind = Column(Enum(LessonKind, native_enum=False))

    group_idx = Index("group_idx", GroupsRelatedModel.group_id)

    query: sql.Select
