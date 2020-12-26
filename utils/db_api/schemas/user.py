from sqlalchemy import Column, BigInteger, sql, SmallInteger, ForeignKey

from utils.db_api.db_gino import TimedBaseModel, BaseModel
from utils.db_api.schemas.schedule import GroupsRelatedModel


class User(GroupsRelatedModel, TimedBaseModel):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    subgroup = Column(SmallInteger, nullable=False)

    query: sql.Select


class UserRelatedModel(BaseModel):
    __abstract__ = True
    user_id = Column(ForeignKey(f"{User.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'),
                     nullable=False)
