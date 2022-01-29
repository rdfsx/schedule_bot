import sqlalchemy as sa
from sqlalchemy.orm import declarative_mixin, declared_attr

from app.db.models.base import TimeBaseModel


class ClassRoomModel(TimeBaseModel):
    id: int = sa.Column(sa.Integer, primary_key=True)
    name: str = sa.Column(sa.String(50), unique=True, nullable=False)


@declarative_mixin
class ClassRoomRelatedModel:
    __abstract__ = True

    @declared_attr
    def classroom_id(self):
        return sa.Column(
            sa.ForeignKey(f"{ClassRoomModel.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'),
        )
