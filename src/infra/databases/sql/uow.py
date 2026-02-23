from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.uow import AbstractUnitOfWork
from src.infra.databases.sql.repositories import (
    SQLUserRepository,
    SQLChannelRepository,
    SQLMessageRepository,
)

__all__ = ["SQLAlchemyUnitOfWork"]


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.user_repo = SQLUserRepository(self.session)
        self.channel_repo = SQLChannelRepository(self.session)
        self.message_repo = SQLMessageRepository(self.session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        try:
            if exc_type is not None:
                await self.rollback()
            else:
                await self.commit()
        finally:
            await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
