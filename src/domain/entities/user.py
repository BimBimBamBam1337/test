from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    SUPERUSER = "superuser"
    USER = "user"


@dataclass
class User:
    id: int
    role: UserRole
    name: str
    username: str
    created_at: datetime

    @classmethod
    def create(cls, tg_data) -> "User":
        return cls(
            id=tg_data.id,
            role=UserRole.USER,
            name=tg_data.name,
            username=tg_data.username,
            created_at=datetime.now(),
        )
