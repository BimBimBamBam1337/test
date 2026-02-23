from datetime import datetime
from typing import Literal, Optional

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
        DateTime, nullable=False, default=datetime.now()
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
