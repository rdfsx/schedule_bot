import typing

import sqlalchemy as sa
from sqlalchemy.orm import declared_attr

from app.db.models.base import TimeBaseModel
from app.db.models.user import UserRelatedModel


class TeacherModel(TimeBaseModel):
    id: int = sa.Column(sa.Integer, primary_key=True, index=True, unique=True)
    first_name: str = sa.Column((sa.String(100)), nullable=False, unique=True)
    surname: str = sa.Column((sa.String(100)), nullable=False)
    patronymic: str = sa.Column((sa.String(100)), nullable=False)
    full_name: str = sa.Column((sa.String(300)), nullable=False, unique=True)

    __table_args__ = (
        sa.UniqueConstraint(first_name, surname, patronymic),
    )


class TeacherRelatedModel:
    __abstract__ = True

    @declared_attr
    def teacher_id(self):
        return sa.Column(
            sa.ForeignKey(f"{TeacherModel.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'),
            nullable=False,
        )


class TeacherRelatedNullModel:
    __abstract__ = True

    @declared_attr
    def teacher_id(self):
        return sa.Column(
            sa.ForeignKey(f"{TeacherModel.__tablename__}.id", ondelete='CASCADE', onupdate='CASCADE'),
        )


class TeacherRatingModel(UserRelatedModel, TeacherRelatedModel, TimeBaseModel):
    id: int = sa.Column(sa.Integer, primary_key=True, index=True, unique=True)
    rate: typing.Literal[1, 2, 3, 4, 5] = sa.Column(sa.SmallInteger, nullable=False)

    rate_idx = sa.Index("rate_idx", UserRelatedModel.user_id, TeacherRelatedModel.teacher_id, unique=True)
