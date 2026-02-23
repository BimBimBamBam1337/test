from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import User, UserRole
from src.domain.repositories import AbstractUserRepository
from src.infra.databases.sql.mappers import UserMapper
from src.infra.databases.sql.models import UserORM


class SQLUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists(self, id: int) -> bool:
        result = await self.session.execute(select(1).where(UserORM.id == id).limit(1))
        return result.scalar() is not None

    async def create(self, entity: User) -> User:
        user_orm = UserMapper.to_orm(entity)
        self.session.add(user_orm)
        await self.session.flush()
        return entity

    async def get_by_id(self, id: int) -> User | None:
        user_orm: UserORM | None = await self.session.get(UserORM, id)
        return UserMapper.to_entity(user_orm) if user_orm else None

    async def get_by_name(self, name: str) -> User | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.name == name).limit(1)
        )
        user_orm: UserORM | None = result.scalar_one_or_none()
        return UserMapper.to_entity(user_orm) if user_orm else None

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.username == username).limit(1)
        )
        user_orm: UserORM | None = result.scalar_one_or_none()
        return UserMapper.to_entity(user_orm) if user_orm else None

    async def update(self, entity: User) -> User | None:
        user_orm = await self.session.get(UserORM, entity.id)
        if user_orm is None:
            return None
        result = await self.session.execute(
            update(UserORM)
            .where(UserORM.id == id)
            .values(**user_orm.__dict__)
            .returning(UserORM)
        )
        await self.session.flush()
        user_orm: UserORM | None = result.scalar_one_or_none()
        return UserMapper.to_entity(user_orm) if user_orm else None

    async def delete(self, id: int) -> User | None:
        result = await self.session.execute(
            delete(UserORM).where(UserORM.id == id).returning(UserORM)
        )
        await self.session.flush()
        user_orm: UserORM | None = result.scalar_one_or_none()
        return UserMapper.to_entity(user_orm) if user_orm else None

    async def get_all(self, by_role: UserRole | None = None) -> list[User]:
        query = select(UserORM)
        if by_role is not None:
            query = query.where(UserORM.role == by_role.value)
        result = await self.session.execute(query)
        users_orm = result.scalars().all()
        return [UserMapper.to_entity(user_orm) for user_orm in users_orm]
