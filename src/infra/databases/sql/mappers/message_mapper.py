from typing import Optional
from pyrogram.types import Message as PyroMessage

from src.domain.entities.message import Message
from src.infra.databases.sql.models import MessageORM


class MessageMapper:
    @staticmethod
    def to_entity(orm: MessageORM) -> Message:
        return Message(
            id=orm.id,
            chat_id=orm.chat_id,
            text=orm.text,
            direction=orm.direction,
            username=orm.username,
            full_name=orm.full_name,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )
