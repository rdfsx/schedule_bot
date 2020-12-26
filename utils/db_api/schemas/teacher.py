from sqlalchemy import Column, String, sql, Integer, UniqueConstraint, ForeignKey

from utils.db_api.db_gino import TimedBaseModel, BaseModel, db
from utils.db_api.schemas.user import UserRelatedModel


class Teacher(TimedBaseModel):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    full_name = Column((String(150)), unique=True, nullable=False)
    rating = Column(Integer, default=0)
    count = Column(Integer, default=0)

    query: sql.Select


class TeacherRelatedModel(BaseModel):
    __abstract__ = True
    teacher_id = Column(ForeignKey(f"{Teacher.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'),
                        nullable=False)


class TeacherRating(UserRelatedModel, TeacherRelatedModel, TimedBaseModel):
    __tablename__ = 'teacher_rating'

    rate = Column(Integer, nullable=False)
    link = Column(String(100))

    __table_args__ = UniqueConstraint(UserRelatedModel.user_id, TeacherRelatedModel.teacher_id)

    query: sql.Select
