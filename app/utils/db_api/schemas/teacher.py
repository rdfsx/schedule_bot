from sqlalchemy import Column, String, sql, Integer, ForeignKey

from app.utils.db_api.db_gino import TimedBaseModel, BaseModel


class Teacher(TimedBaseModel):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    full_name = Column((String(150)), nullable=False)
    rating = Column(Integer, default=0)
    count = Column(Integer, default=0)

    query: sql.Select


class TeacherRelatedModel(BaseModel):
    __abstract__ = True
    teacher_id = Column(ForeignKey(f"{Teacher.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'),
                        nullable=False)


class TeacherRelatedModelNull(BaseModel):
    __abstract__ = True
    teacher_id = Column(ForeignKey(f"{Teacher.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'))
