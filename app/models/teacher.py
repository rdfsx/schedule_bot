from sqlalchemy import Column, String, Integer, ForeignKey, Index, UniqueConstraint

from app.models.base import TimedBaseModel
from app.models.user import UserRelatedModel


class TeacherModel(TimedBaseModel):
    __tablename__ = 'teacher'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    full_name = Column((String(150)), nullable=False)
    rating = Column(Integer, default=0)
    count = Column(Integer, default=0)


class TeacherRelatedModel:
    __abstract__ = True

    teacher_id = Column(
        ForeignKey(f"{TeacherModel.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    )


class TeacherRelatedModelNull:
    __abstract__ = True

    teacher_id = Column(
        ForeignKey(f"{TeacherModel.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'),
    )


class TeacherRating(UserRelatedModel, TeacherRelatedModel, TimedBaseModel):
    __tablename__ = 'teacher_rating'

    rate = Column(Integer, nullable=False)

    rate_idx = Index("rate_idx", UserRelatedModel.user_id, TeacherRelatedModel.teacher_id)

    __table_args__ = UniqueConstraint(UserRelatedModel.user_id, TeacherRelatedModel.teacher_id)
