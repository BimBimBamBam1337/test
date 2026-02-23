from datetime import datetime
from pyrogram.types import Chat as PyroChat

from src.domain.entities import Channel


class PyroChannelMapper:
    @staticmethod
    def to_entity(chat: PyroChat) -> Channel:
        return Channel(
            id=chat.id,
            title=chat.title,
            is_scam=False,
            created_at=datetime.now(),
        )
