from datetime import datetime
from typing import Literal, Optional

from domain.entities import Message
from sqlalchemy import BIGINT, String, DateTime
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from .base import Base


class MessageORM(Base):
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

    @classmethod
    def from_entity(cls, entity: Message) -> "MessageORM":
        return cls(
            id=entity.id,
            chat_id=entity.chat_id,
            text=entity.text,
            direction=entity.direction,
            username=entity.username,
            full_name=entity.full_name,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
