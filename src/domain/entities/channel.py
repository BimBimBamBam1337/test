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
    title: str
    is_scam: bool
    created_at: datetime

    @classmethod
    def create(
        cls,
        id: int,
        title: str,
        is_scam: bool,
    ) -> "Channel":
        return cls(
            id=id,
            title=title,
            is_scam=is_scam,
            created_at=datetime.now(),
        )
