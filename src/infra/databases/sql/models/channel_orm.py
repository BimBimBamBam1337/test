from datetime import datetime

from sqlalchemy import BIGINT, BOOLEAN, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.entities import Language, ChannelType, Channel

from .base import Base


class ChannelORM(Base):
    __tablename__ = "channel"
    id: Mapped[int] = mapped_column(BIGINT, nullable=False, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    is_scam: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    @staticmethod
    def from_entity(entity: Channel) -> "ChannelORM":
        return ChannelORM(
            id=entity.id,
            title=entity.title,
            created_at=entity.created_at,
            is_scam=entity.is_scam,
        )
