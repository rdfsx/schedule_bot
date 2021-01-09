from app.models.base import TimedBaseModel
from sqlalchemy import Column, ForeignKey, BigInteger, String


class Chat(TimedBaseModel):
    __tablename__ = "chats"

    id = Column(BigInteger, primary_key=True, index=True)
    type = Column(String)


class ChatRelatedMixin:
    chat_id = Column(
        ForeignKey(f"{Chat.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
