from typing import Optional
from pyrogram.types import Message as PyroMessage

from src.domain.entities.message import Message
from src.infra.databases.sql.models import MessageORM


class PyroMessageMapper:

    @staticmethod
    def to_entity(message: PyroMessage) -> Message:
        if message.text is None and message.caption is None:
            raise ValueError("Message text is empty")
        outgoing = message.from_user.is_self
        direction = "out" if outgoing else "in"

        if message.outgoing:
            chat_id = message.chat.id
        else:
            if message.from_user:
                chat_id = message.from_user.id
            else:
                chat_id = message.chat.id

        if message.outgoing:
            username: Optional[str] = message.chat.username
        else:
            username = message.from_user.username if message.from_user else None

        if message.outgoing:
            first_name = message.chat.first_name or ""
            last_name = message.chat.last_name or ""
        else:
            if message.from_user:
                first_name = message.from_user.first_name or ""
                last_name = message.from_user.last_name or ""
            else:
                first_name = ""
                last_name = ""

        full_name = f"{first_name} {last_name}".strip() or None

        return Message(
            id=message.id,
            chat_id=chat_id,
            text=message.text or message.caption,
            direction=direction,
            username=username,
            full_name=full_name,
            created_at=message.date,
            updated_at=None,
        )

    @staticmethod
    def to_orm(message: PyroMessage) -> MessageORM:

        if message.text is None and message.caption is None:
            raise ValueError("Message text is empty")
        outgoing = message.from_user.is_self
        direction = "out" if outgoing else "in"

        if message.outgoing:
            chat_id = message.chat.id
        else:
            chat_id = message.from_user.id if message.from_user else message.chat.id

        if message.outgoing:
            username: Optional[str] = message.chat.username
        else:
            username = message.from_user.username if message.from_user else None

        if message.outgoing:
            first_name = message.chat.first_name or ""
            last_name = message.chat.last_name or ""
        else:
            if message.from_user:
                first_name = message.from_user.first_name or ""
                last_name = message.from_user.last_name or ""
            else:
                first_name = ""
                last_name = ""

        full_name = f"{first_name} {last_name}".strip() or None

        return MessageORM(
            id=message.id,
            chat_id=chat_id,
            text=message.text or message.caption,
            username=username,
            full_name=full_name,
            direction=direction,
            created_at=message.date,
            updated_at=None,
        )
