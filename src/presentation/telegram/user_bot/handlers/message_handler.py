from loguru import logger

from loguru import logger
from pyrogram.client import Client
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from src.infra.databases.sql.uow import SQLAlchemyUnitOfWork
from src.presentation.telegram.mappers import (
    PyroMessageMapper,
)
from src.infra.databases.sql.session import SessionFactory


async def handler_new_message(
    client: Client,
    message: Message,
):
    """Обработка новых сообщений."""
    entity = PyroMessageMapper.to_entity(message)
    uow = SQLAlchemyUnitOfWork(session_factory=SessionFactory)
    async with uow:
        db_message = await uow.message_repo.add_message(entity)
        logger.debug(f"Новое сообщение: {db_message}")


async def handler_message_deleted(client: Client, messages):
    """Обработка удаленных сообщений."""
    admins = [8140271247]
    uow = SQLAlchemyUnitOfWork(session_factory=SessionFactory)

    async with uow:
        for message in messages:

            old_message = await uow.message_repo.get_message(message.id)

            if not old_message:
                continue

            if old_message.direction == "out":
                logger.debug(f"Старое сообщение перед удалением: {old_message}")

                await uow.message_repo.delete_message(message.id)
                logger.info(f"Сообщение с ID {message.id} удалено из базы данных")

                for admin in admins:
                    try:
                        await client.send_message(
                            chat_id=admin,
                            text=f"""
🗑Менеджер удалил сообщение:

<u>Чат:</u>
id = <b>{old_message.chat_id}</b>
username = <b>{'@' + old_message.username if old_message.username else ''}</b>
name = <b>{old_message.full_name}</b>

<u>Сообщение:</u>
id = <b>{old_message.id}</b>
дата отправки: <b>{old_message.created_at.strftime('%Y-%m-%d %H:%M:%S')}</b>

<u>Текст:</u>
{old_message.text}
""",
                            parse_mode=ParseMode.HTML,
                        )
                    except Exception as e:
                        logger.error(
                            f"Не удалось отправить уведомление админу {admin}: {e}"
                        )


async def handler_message_edited(
    client: Client,
    message: Message,
):
    uow = SQLAlchemyUnitOfWork(session_factory=SessionFactory)
    """Обработка редактированных сообщений."""
    admins = [8140271247]
    async with uow:
        old_message = await uow.message_repo.get_message(message.id)
        if not old_message:
            logger.warning(f"Сообщение {message.id} не найдено в базе")
            return

        if old_message.direction == "out":
            logger.debug(f"Старое сообщение перед обновлением: {old_message}")

            old_text = old_message.text
            old_message.text = message.text
            updated_message = await uow.message_repo.update_message(old_message)
            logger.debug(f"Сообщение обновлено: {updated_message}")

            for admin in admins:
                try:
                    await client.send_message(
                        chat_id=admin,
                        text=f"""
    🔄 Сообщение обновлено:

    <u>Чат:</u>
    id = <b>{message.chat.id}</b>
    username = <b>{'@' + message.chat.username if message.chat.username else ''}</b>
    name = <b>{message.chat.first_name} {message.chat.last_name or ''}</b>

    <u>Сообщение:</u>
    id = <b>{updated_message.id}</b>
    дата отправки: <b>{updated_message.created_at.strftime('%Y-%m-%d %H:%M:%S')}</b>
    дата обновления: <b>{updated_message.updated_at.strftime('%Y-%m-%d %H:%M:%S')}</b>

    <u>Старый текст:</u>
    {old_text}

    <u>Новый текст:</u>
    {updated_message.text}
    """,
                        parse_mode=ParseMode.HTML,
                    )
                except Exception as e:
                    logger.error(f"Не удалось отправить сообщение админу {admin}: {e}")
