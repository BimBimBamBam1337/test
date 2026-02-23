from datetime import datetime

from pyrogram.types import User as PyroUser

from domain.entities import User, UserRole


class PyroUserMapper:

    @staticmethod
    def to_entity(user: PyroUser) -> User:
        return User(
            id=user.id,
            role=UserRole.USER,
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.first_name if user.first_name and user.last_name else None,
            username=user.username,
            created_at=datetime.now(),
        )
