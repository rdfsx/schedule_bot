from sqlalchemy import Column, BigInteger, sql, SmallInteger, ForeignKey

from app.utils import TimedBaseModel, BaseModel
from app.utils import GroupsRelatedModel


class User(GroupsRelatedModel, TimedBaseModel):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, unique=True)
    subgroup = Column(SmallInteger)

    query: sql.Select


class UserRelatedModel(BaseModel):
    __abstract__ = True
    user_id = Column(ForeignKey(f"{User.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'),
                     nullable=False)
