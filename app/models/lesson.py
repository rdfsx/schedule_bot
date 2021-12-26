from sqlalchemy import Integer, Column, String, ForeignKey

from app.models.base import TimedBaseModel


class LessonModel(TimedBaseModel):
    __tablename__ = 'lesson'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    lesson = Column(String(300), nullable=False, unique=True)


class LessonRelatedModel:
    __abstract__ = True

    lesson_id = Column(
        ForeignKey(f"{LessonModel.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    )
