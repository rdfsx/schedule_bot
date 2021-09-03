from sqlalchemy import Column, String, sql, Integer, SmallInteger, Enum, ForeignKey

from app.enums.fuckult import Fuckult
from app.utils.db_api.db_gino import TimedBaseModel, BaseModel


class Groups(TimedBaseModel):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, unique=True)
    group = Column(String(20), unique=True, nullable=False)
    fuck = Column(Enum(Fuckult, native_enum=False), nullable=False)
    subgroups = Column(SmallInteger, nullable=False)

    query: sql.Select


class GroupsRelatedModel(BaseModel):
    __abstract__ = True

    group_id = Column(ForeignKey(f"{Groups.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'))
