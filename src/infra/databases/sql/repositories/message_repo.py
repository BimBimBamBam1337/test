from datetime import datetime
from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pyrogram.types import Message as PyroMessage

from src.domain.repositories import AbstractMessageRepository
from src.domain.entities import Message
from src.infra.databases.sql.mappers import PyroMessageMapper
from src.infra.databases.sql.models import MessageORM


class SQLMessageRepository(AbstractMessageRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_message(self, message: PyroMessage) -> Message:
        message_orm = PyroMessageMapper.to_orm(message)
        self.session.add(message_orm)
        return PyroMessageMapper.to_entity(message)

    async def get_message(self, message_id: int) -> Message | None:

        result = await self.session.execute(
            select(MessageORM).where(MessageORM.id == message_id)
        )
        message_orm: MessageORM | None = result.scalar_one_or_none()
        return PyroMessageMapper.to_entity(message_orm) if message_orm else None

    async def get_last_message(self, chat_id: int) -> Message:
        result = await self.session.execute(
            select(MessageORM)
            .where(MessageORM.chat_id == chat_id)
            .order_by(MessageORM.created_at.desc())
        )
        message_orm: MessageORM = result.scalar_one_or_none()
        return PyroMessageMapper.to_entity(message_orm)

    async def update_message(self, message: Message) -> Message:
        message.updated_at = datetime.now()
        self.session.add(message)
        return message

    async def delete_message(self, message_id: int) -> None:
        await self.session.execute(
            delete(MessageORM).where(MessageORM.id == message_id)
        )
