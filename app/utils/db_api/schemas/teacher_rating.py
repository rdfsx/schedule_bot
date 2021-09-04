from sqlalchemy import Column, Integer, String, Index, UniqueConstraint, sql

from app.utils.db_api.db_gino import TimedBaseModel
from app.utils.db_api.schemas.teacher import TeacherRelatedModel
from app.utils.db_api.schemas.user import UserRelatedModel


class TeacherRating(UserRelatedModel, TeacherRelatedModel, TimedBaseModel):
    __tablename__ = 'teacher_rating'

    rate = Column(Integer, nullable=False)
    link = Column(String(100))

    rate_idx = Index("rate_idx", UserRelatedModel.user_id, TeacherRelatedModel.teacher_id)

    __table_args__ = UniqueConstraint(UserRelatedModel.user_id, TeacherRelatedModel.teacher_id)

    query: sql.Select
