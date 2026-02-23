from datetime import datetime

from sqlalchemy import BIGINT, BOOLEAN, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.entities import Language, ChannelType

from .base import Base


class ChannelORM(Base):
    __tablename__ = "channel"
    id: Mapped[int] = mapped_column(BIGINT, nullable=False, primary_key=True)
    language: Mapped[Language] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    type: Mapped[ChannelType] = mapped_column(String, nullable=True)
    link: Mapped[str] = mapped_column(String, nullable=False)
    is_verified: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, default=False)
    is_scam: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
