from datetime import datetime
from typing import Optional

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repositories import AbstractMessageRepository
from src.domain.entities import Message
from src.infra.databases.sql.mappers import MessageMapper
from src.infra.databases.sql.models import MessageORM


class SQLMessageRepository(AbstractMessageRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_message(self, message: Message) -> Message:
        message_orm = MessageORM.from_entity(message)
        self.session.add(message_orm)
        return message

    async def get_message(self, message_id: int) -> Message | None:
        result = await self.session.execute(
            select(MessageORM).where(MessageORM.id == message_id)
        )
        message_orm: MessageORM | None = result.scalar_one_or_none()
        return MessageMapper.to_entity(message_orm) if message_orm else None

    async def get_last_message(self, chat_id: int) -> Message:
        result = await self.session.execute(
            select(MessageORM)
            .where(MessageORM.chat_id == chat_id)
            .order_by(MessageORM.created_at.desc())
        )
        message_orm: MessageORM = result.scalar_one_or_none()
        return MessageMapper.to_entity(message_orm)

    async def update_message(self, message: Message) -> Message:
        stmt = (
            update(MessageORM)
            .where(MessageORM.id == message.id)
            .values(
                text=message.text,
                updated_at=datetime.now(),
            )
            .returning(MessageORM)
        )

        result = await self.session.execute(stmt)
        message_orm: MessageORM = result.scalar_one_or_none()
        return MessageMapper.to_entity(message_orm)

    async def delete_message(self, message_id: int) -> None:
        await self.session.execute(
            delete(MessageORM).where(MessageORM.id == message_id)
        )
