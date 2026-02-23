from abc import ABC, abstractmethod

from src.domain.entities import Channel, ChannelType


class AbstractChannelRepository(ABC):
    async def exists(self, id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def create(self, entity: Channel) -> Channel:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> Channel | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_title(self, title: str) -> Channel | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_type(self, type: str) -> list[Channel] | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: Channel) -> Channel | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> Channel | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, type: ChannelType | None = None) -> list[Channel]:
        raise NotImplementedError
