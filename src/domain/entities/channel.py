from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class Language(Enum):
    RU = "RU"
    EN = "EN"


class ChannelType(Enum):
    SENDER = "sender"
    RECIVIER = "recivier"


@dataclass
class Channel:
    id: int
    language: Language
    title: str
    type: ChannelType | None
    link: str
    is_verified: bool
    is_scam: bool
    created_at: datetime

    @classmethod
    def create(cls, tg_data) -> "Channel":
        return cls(
            id=tg_data.id,
            language=Language.RU,
            title=tg_data.title,
            type=None,
            link=tg_data.link,
            is_verified=False,
            is_scam=False,
            created_at=datetime.now(),
        )
