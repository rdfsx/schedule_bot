from sqlalchemy import Column, ForeignKey, Integer, String

from app.models.base import TimedBaseModel


class Group(TimedBaseModel):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, unique=True)
    group = Column(String(20), unique=True, nullable=False)
    fuck = Column(Enum(Fuckult, native_enum=False), nullable=False)
    subgroups = Column(SmallInteger, nullable=False)


class GroupsRelatedModel:
    __abstract__ = True

    group_id = Column(
        ForeignKey(f"{Group.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'),
    )
