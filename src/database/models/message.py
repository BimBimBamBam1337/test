from datetime import datetime
from typing import Literal, Optional
from pyrogram.types import Message as PyroMessage
from sqlalchemy import (
    BIGINT,
    String,
    DateTime,
    String,
)
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from .base import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True, default=None)
    full_name: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, default=None
    )
    direction: Mapped[Literal["in", "out"]] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    @staticmethod
    def from_pyro(message: PyroMessage) -> "Message":
        print(message)
        if message.text is None and message.caption is None:
            raise ValueError("Message text is empty")
        outgoing = message.from_user.is_self if message.from_user else message.outgoing
        direction = "out" if outgoing else "in"

        if message.outgoing:
            chat_id = message.chat.id
        else:
            chat_id = message.from_user.id if message.from_user else message.chat.id

        if message.outgoing:
            username: Optional[str] = message.chat.username
        else:
            username = message.from_user.username if message.from_user else None

        if message.outgoing:
            first_name = message.chat.first_name or ""
            last_name = message.chat.last_name or ""
        else:
            if message.from_user:
                first_name = message.from_user.first_name or ""
                last_name = message.from_user.last_name or ""
            else:
                first_name = ""
                last_name = ""

        full_name = f"{first_name} {last_name}".strip() or None

        return Message(
            id=message.id,
            chat_id=chat_id,
            text=message.text or message.caption,
            username=username,
            full_name=full_name,
            direction=direction,
            created_at=message.date,
            updated_at=None,
        )
