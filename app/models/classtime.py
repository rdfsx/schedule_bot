import sqlalchemy as sa
from sqlalchemy.orm import declared_attr

from app.models.base import TimeBaseModel


class ClassTimeModel(TimeBaseModel):
    id: int = sa.Column(sa.Integer, primary_key=True)
    number: int = sa.Column(sa.SmallInteger, unique=True, nullable=False)
    interval_before_break: str = sa.Column(sa.String(20))
    interval_after_break: str = sa.Column(sa.String(20))
    full_interval: str = sa.Column(sa.String(20), nullable=False, unique=True)


class ClassTimeRelatedModel:
    __abstract__ = True

    @declared_attr
    def classtime_id(self):
        return sa.Column(
            sa.ForeignKey(f"{ClassTimeModel.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'),
        )
