from sqlalchemy import Column, ForeignKey, Integer, String, Enum, SmallInteger

from app.enums.fuckult import Fuckult
from app.models.base import TimedBaseModel


class GroupModel(TimedBaseModel):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(20), unique=True, nullable=False)
    fuck = Column(Enum(Fuckult, native_enum=False), nullable=False)
    subgroup = Column(SmallInteger, nullable=False)


class GroupRelatedModel:
    __abstract__ = True

    group_id = Column(
        ForeignKey(f"{GroupModel.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'),
    )
