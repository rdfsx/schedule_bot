from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TimedBaseModel(Base):
    __abstract__ = True
    __mapper_args__ = {"eager_defaults": True}

    created_at = Column(DateTime(True), server_default=func.now())
    updated_at = Column(DateTime(True),
                        default=func.now(),
                        onupdate=func.now(),
                        server_default=func.now())
