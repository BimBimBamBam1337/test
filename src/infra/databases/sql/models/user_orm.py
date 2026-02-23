from datetime import datetime

from sqlalchemy import BIGINT, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.entities import UserRole

from .base import Base


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
