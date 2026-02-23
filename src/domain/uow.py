from abc import ABC, abstractmethod

from src.domain.repositories import (
    AbstractChannelRepository,
    AbstractUserRepository,
    AbstractMessageRepository,
)

__all__ = ["AbstractUnitOfWork"]


class AbstractUnitOfWork(ABC):
    user_repo: AbstractUserRepository
    channel_repo: AbstractChannelRepository
    message_repo: AbstractMessageRepository

    @abstractmethod
    async def __aenter__(self) -> "AbstractUnitOfWork": ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None: ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
