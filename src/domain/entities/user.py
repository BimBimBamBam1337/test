from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    SUPERUSER = "superuser"
    USER = "user"


@dataclass
class User:
    id: int
    role: UserRole
    first_name: str
    last_name: str
    full_name: str | None
    username: str
    created_at: datetime

    @classmethod
    def create(
        cls,
        id: int,
        role: UserRole,
        first_name: str,
        last_name: str,
        full_name: str,
        username: str,
    ) -> "User":
        return cls(
            id=id,
            role=UserRole.USER,
            first_name=first_name,
            last_name=last_name,
            full_name=first_name if first_name and last_name else None,
            username=username,
            created_at=datetime.now(),
        )
