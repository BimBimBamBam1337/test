import asyncio

from datetime import datetime, timedelta
from pyrogram.client import Client
from pyrogram.types import Message, ChatJoiner
from pyrogram.enums import ParseMode
from pyrogram.enums import ChatType
from loguru import logger

from conf import CHANNEL, HELLO_MSG
from src.database.repositories import MessageRepository, UserRepository
from src.database.models import Message, User
from src.database.session import SessionFactory
from src.database.models import Message
from src.database.exceptions import DBError, MessageEmpty, UserNotFoundError


async def polling_chat_request(client: Client):
    message_repo = MessageRepository(session=SessionFactory)  # type: ignore
    user_repo = UserRepository(session=SessionFactory)
    chat = await client.get_chat(CHANNEL)
    # chat = await client.get_chat("https://t.me/+jCX3RyK5zMRjOGMy")
    while True:
        try:
            async for request in client.get_chat_join_requests(chat.id):  # type: ignore
                try:
                    if not isinstance(request, ChatJoiner):
                        continue

                    now_dt = datetime.now()
                    if (now_dt - request.date) > timedelta(seconds=1):
                        await asyncio.sleep(5)
                        res = await client.approve_chat_join_request(
                            chat.id, request.user.id
                        )
                        if res:
                            logger.info(f"Approve in {chat.title}: {request.user.id}")

                        try:
                            user = await user_repo.get_user_by_id(request.user.id)
                        except UserNotFoundError:

                            user = await user_repo.create_user(
                                User.from_pyro(request.user)
                            )
                            logger.info(f"New user created: {user}")
                            await asyncio.sleep(3)
                            msg = await client.send_message(
                                user.id,
                                HELLO_MSG,
                            )
                            await message_repo.add_message(Message.from_pyro(msg))
                except Exception as e:
                    logger.error(f"Handle chat request: {e}")
        except Exception as e:
            logger.error(f"Polling chat request: {e}")
        await asyncio.sleep(15)


async def fetch_missing_messages(client: Client):
    """Получение и сохранение недостающих сообщений из всех приватных чатов."""
    message_repo = MessageRepository(session=SessionFactory)
    async for dialog in client.get_dialogs():  # type: ignore
        if dialog.chat.type == ChatType.PRIVATE:
            try:
                last_message_id = (
                    await message_repo.get_last_message(dialog.chat.id)
                ).id
            except DBError:
                last_message_id = 0

            if dialog.top_message.id == last_message_id:
                continue

            async for message in client.get_chat_history(  # type: ignore
                dialog.chat.id, offset_id=last_message_id  # type: ignore
            ):
                try:
                    db_message = await message_repo.add_message(
                        Message.from_pyro(message)
                    )
                    logger.debug(f"Добавлено {db_message}")
                except MessageEmpty:
                    pass
                except DBError as e:
                    logger.error(f"Ошибка при добавлении сообщения: {e}")


async def handler_new_message(
    client: Client,
    message: Message,
):
    """Обработка новых сообщений."""
    message_repo = MessageRepository(session=SessionFactory)  # type: ignore

    db_message = await message_repo.add_message(Message.to_orm(message))
    logger.debug(f"Новое сообщение: {str(db_message)}")


async def handler_message_deleted(client: Client, messages):
    """Обработка удаленных сообщений."""
    admins = [8140271247]
    message_repo = MessageRepository(session=SessionFactory)  # type: ignore

    for message in messages:

        old_message = await message_repo.get_message(message.id)

        if not old_message:
            continue

        if old_message.direction == "out":
            logger.debug(f"Старое сообщение перед удалением: {old_message}")

            await message_repo.delete_message(message.id)
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
    message_repo = MessageRepository(session=SessionFactory)  # type: ignore
    """Обработка редактированных сообщений."""
    admins = [8140271247]

    old_message = await message_repo.get_message(message.id)
    if not old_message:
        logger.warning(f"Сообщение {message.id} не найдено в базе")
        return

    if old_message.direction == "out":
        logger.debug(f"Старое сообщение перед обновлением: {old_message}")

        old_text = old_message.text
        old_message.text = message.text
        updated_message = await message_repo.update_message(old_message)
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
