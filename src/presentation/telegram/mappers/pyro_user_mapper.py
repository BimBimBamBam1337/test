from datetime import datetime

from pyrogram.types import User as PyroUser

from domain.entities import User, UserRole


class PyroUserMapper:

    @staticmethod
    def to_entity(user: PyroUser) -> User:
        return User(
            id=user.id,
            role=UserRole.USER,
            name=user.name,
            username=user.username,
            created_at=datetime.now(),
        )
