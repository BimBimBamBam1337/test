from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Channel
from src.domain.entities.channel import ChannelType
from src.domain.repositories import AbstractChannelRepository
from src.infra.databases.sql.mappers import ChannelMapper
from src.infra.databases.sql.models import ChannelORM


class SQLChannelRepository(AbstractChannelRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists(self, id: int) -> bool:
        result = await self.session.execute(
            select(1).where(ChannelORM.id == id).limit(1)
        )
        return result.scalar() is not None

    async def create(self, entity: Channel) -> Channel:
        channel_orm = ChannelORM.to_orm(entity)
        self.session.add(channel_orm)
        await self.session.flush()
        return entity

    async def get_by_id(self, id: int) -> Channel | None:
        channel_orm: ChannelORM | None = await self.session.get(ChannelORM, id)
        return ChannelMapper.to_entity(channel_orm) if channel_orm else None

    async def get_by_type(self, type: str) -> list[Channel] | None:
        result = await self.session.execute(
            select(ChannelORM).where(ChannelORM.type == type)
        )
        channels_orm = result.scalars().all()
        return [ChannelMapper.to_entity(channel_orm) for channel_orm in channels_orm]

    async def get_by_title(self, title: str) -> Channel | None:
        result = await self.session.execute(
            select(ChannelORM).where(ChannelORM.name == title).limit(1)
        )
        channel_orm: ChannelORM | None = result.scalar_one_or_none()
        return ChannelMapper.to_entity(channel_orm) if channel_orm else None

    async def update(self, entity: Channel) -> Channel | None:
        channel_orm = await self.session.get(ChannelORM, entity.id)
        if channel_orm is None:
            return None
        result = await self.session.execute(
            update(ChannelORM)
            .where(ChannelORM.id == id)
            .values(**channel_orm.__dict__)
            .returning(ChannelORM)
        )
        await self.session.flush()
        channel_orm: ChannelORM | None = result.scalar_one_or_none()
        return ChannelMapper.to_entity(channel_orm) if channel_orm else None

    async def delete(self, id: int) -> Channel | None:
        result = await self.session.execute(
            delete(ChannelORM).where(ChannelORM.id == id).returning(ChannelORM)
        )
        await self.session.flush()
        channel_orm: ChannelORM | None = result.scalar_one_or_none()
        return ChannelMapper.to_entity(channel_orm) if channel_orm else None

    async def get_all(self, type: ChannelType | None = None) -> list[Channel]:
        query = select(ChannelORM)
        if type is not None:
            result = await self.session.execute(query)
            query = select(ChannelORM).where(ChannelORM.type == type)
        result = await self.session.execute(query)
        channels_orm = result.scalars().all()
        return [ChannelMapper.to_entity(channel_orm) for channel_orm in channels_orm]
