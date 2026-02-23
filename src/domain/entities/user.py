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
    def create(
        cls,
        id: int,
        role: UserRole,
        name: str,
        username: str,
    ) -> "User":
        return cls(
            id=id,
            role=UserRole.USER,
            name=name,
            username=username,
            created_at=datetime.now(),
        )
