from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal


@dataclass
class Message:
    id: int
    chat_id: int
    text: str
    direction: Literal["in", "out"]
    username: Optional[str]
    full_name: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    @classmethod
    def create(
        cls,
        id: int,
        chat_id: int,
        text: str,
        direction: Literal["in", "out"],
        username: Optional[str] = None,
        full_name: Optional[str] = None,
    ) -> "Message":
        return cls(
            id=id,
            chat_id=chat_id,
            text=text,
            direction=direction,
            username=username,
            full_name=full_name,
            created_at=datetime.now(),
            updated_at=None,
        )
