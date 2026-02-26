from datetime import datetime
from typing import Literal, Optional
from pyrogram.types import User as PyroUser
from sqlalchemy import (
    BIGINT,
    String,
    DateTime,
    String,
    Boolean,
    JSON,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class AutoPilotStatus(Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


class UserStatus(Enum):
    LEAD = "lead"
    VIP = "vip"
    PREMIUM = "premium"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    full_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True, unique=True)

    status: Mapped[str] = mapped_column(String, default=UserStatus.LEAD)
    autopilot_status: Mapped[str] = mapped_column(
        String, default=AutoPilotStatus.DISABLED
    )

    language_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    autopilot: Mapped[bool] = mapped_column(Boolean, default=False)
    autosending: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), nullable=False
    )

    @staticmethod
    def from_pyro(pyro_user: PyroUser) -> "User":

        full_name = (pyro_user.first_name or "") + " " + (pyro_user.last_name or "")
        return User(
            id=pyro_user.id,
            username=pyro_user.username,
            full_name=full_name.strip() or None,
            language_code=getattr(pyro_user, "lang_code", None),
            created_at=datetime.now(),
        )
