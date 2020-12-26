from sqlalchemy import Column, String, sql, Integer, ForeignKey, SmallInteger
from sqlalchemy import Enum

from models.week import UnderAboveWeek, Week
from utils.db_api.db_gino import TimedBaseModel, BaseModel
from utils.db_api.schemas.group import GroupsRelatedModel


class Lessons(TimedBaseModel):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True)
    lesson = Column(String(300), nullable=False, unique=True)

    query: sql.Select


class LessonsRelatedModel(BaseModel):
    __abstract__ = True
    lesson_id = Column(ForeignKey(f"{Lessons.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'),
                       nullable=False)


class Timetable(GroupsRelatedModel, LessonsRelatedModel, TimedBaseModel):
    __tablename__ = 'timetables'

    id = Column(Integer, primary_key=True)
    day_week = Column(Enum(Week, native_enum=False), nullable=False)
    lesson_time = Column(String(20))
    lesson_num = Column(SmallInteger)
    week = Column(Enum(UnderAboveWeek, native_enum=False), nullable=False)
    subgroup = Column(SmallInteger, nullable=False)

    query: sql.Select
