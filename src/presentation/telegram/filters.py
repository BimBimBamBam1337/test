from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject

from infra.databases.sql.uow import SQLAlchemyUnitOfWork


class AdminFilter(BaseFilter):
    async def __call__(self, event: TelegramObject, uow: SQLAlchemyUnitOfWork) -> bool:
        async with uow:
            user = await uow.user_repo.get_by_id(event.from_user.id)
            if user is not None and user.role == "admin":
                return True
            return False
