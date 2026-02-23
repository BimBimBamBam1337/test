from abc import ABC, abstractmethod

from src.domain.entities import User
from src.domain.entities.channel import ChannelType


class AbstractUserRepository(ABC):
    async def exists(self, id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def create(self, entity: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: User) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[User]:
        raise NotImplementedError
