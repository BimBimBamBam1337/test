from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities import Message


class AbstractMessageRepository(ABC):

    @abstractmethod
    async def add_message(self, message: Message) -> Message:
        pass

    @abstractmethod
    async def get_message(self, message_id: int) -> Message | None:
        pass

    @abstractmethod
    async def get_last_message(self, chat_id: int) -> Message:
        pass

    @abstractmethod
    async def update_message(self, message: Message) -> Message:
        pass

    @abstractmethod
    async def delete_message(self, message_id: int) -> None:
        pass
