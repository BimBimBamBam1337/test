from datetime import datetime
from loguru import logger
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.database.models import Message
from src.database.exceptions import DBError


class MessageRepository:

    def __init__(self, session):
        self.session = session()

    async def add_message(self, message: Message) -> Message:
        """Добавление сообщения в базу данных."""

        try:
            self.session.add(message)
            await self.session.commit()
            logger.info(f"Сообщение добавлено: {message}")
            return message
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Ошибка при добавлении сообщения: {e}")
            raise DBError(f"Ошибка при добавлении сообщения: {e}")

    async def get_message(self, message_id: int) -> Message:
        """Получение сообщения по его ID."""

        try:
            result = await self.session.execute(  # type: ignore
                select(Message).where(Message.id == message_id)  # type: ignore
            )
            message = result.scalars().first()
            if message:
                logger.debug(f"Сообщение получено: {message}")
                return message
            else:
                raise DBError(f"Сообщение с ID {message_id} не найдено")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении сообщения: {e}")
            raise DBError(f"Ошибка при получении сообщения: {e}")

    async def get_last_message(self, chat_id: int) -> Message:
        """Получение последнего сообщения из чата."""

        try:
            result = await self.session.execute(
                select(Message)
                .where(Message.chat_id == chat_id)  # type: ignore
                .order_by(Message.created_at.desc())  # type: ignore
            )
            message = result.scalars().first()
            if message:
                logger.debug(f"Последнее сообщение получено: {message}")
                return message
            else:
                raise DBError(f"Сообщений для чата с ID {chat_id} не найдено")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении последнего сообщения: {e}")
            raise DBError(f"Ошибка при получении последнего сообщения: {e}")

    async def update_message(self, message: Message) -> Message:
        """Обновление текста сообщения."""

        try:
            message.updated_at = datetime.now()
            self.session.add(message)
            await self.session.commit()
            logger.info(f"Сообщение обновлено: {message}")
            return message
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Ошибка при обновлении сообщения: {e}")
            raise DBError(f"Ошибка при обновлении сообщения: {e}")

    async def delete_message(self, message_id: int) -> None:
        """Удаление сообщения по его ID."""

        try:
            await self.session.execute(  # type: ignore
                delete(Message).where(Message.id == message_id)  # type: ignore
            )
            await self.session.commit()
            logger.info(f"Сообщение с ID {message_id} удалено")
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Ошибка при удалении сообщения: {e}")
            raise DBError(f"Ошибка при удалении сообщения: {e}")
