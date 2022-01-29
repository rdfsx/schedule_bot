import typing
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr, has_inherited_table
from sqlalchemy.util import ImmutableProperties

Base = declarative_base()
metadata = Base.metadata


class BaseModel(Base):
    __abstract__ = True
    __mapper_args__ = {"eager_defaults": True}

    @declared_attr
    def __tablename__(self) -> str | None:
        if not has_inherited_table(typing.cast(typing.Type[Base], self)):
            return typing.cast(typing.Type[Base], self).__qualname__.lower() + "s"
        return None

    def _get_attributes(self) -> dict[typing.Any, typing.Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def __str__(self) -> str:
        attributes = "|".join(str(v) for k, v in self._get_attributes().items())
        return f"{self.__class__.__qualname__} {attributes}"

    def __repr__(self) -> str:
        table_attrs = typing.cast(ImmutableProperties, sa.inspect(self).attrs)
        primary_keys = " ".join(
            f"{key.name}={table_attrs[key.name].value}"
            for key in sa.inspect(self.__class__).primary_key
        )
        return f"{self.__class__.__qualname__}->{primary_keys}"

    def as_dict(self) -> dict[typing.Any, typing.Any]:
        return self._get_attributes()


class TimeBaseModel(BaseModel):
    __abstract__ = True

    created_at: datetime = sa.Column(sa.DateTime(True), server_default=sa.func.now())
    updated_at: datetime = sa.Column(sa.DateTime(True),
                                     default=sa.func.now(),
                                     onupdate=sa.func.now(),
                                     server_default=sa.func.now())
