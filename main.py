import asyncio

from loguru import logger

from src.config import app
from loguru import logger
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from src.config import app
from src.infra.databases.sql.uow import SQLAlchemyUnitOfWork
from src.infra.databases.sql.mappers import PyroMessageMapper
from src.infra.databases.sql.session import SessionFactory


@app.on_message(filters.private & ~filters.bot, group=-1)
async def handler_new_message(
    client: Client,
    message: Message,
):
    """Обработка новых сообщений."""
    entity = PyroMessageMapper.to_entity(message)
    uow = SQLAlchemyUnitOfWork(session_factory=SessionFactory)
    async with uow:
        print(message.raw.out)
        db_message = await uow.message_repo.add_message(entity)
        logger.debug(f"Новое сообщение: {db_message}")


@app.on_deleted_messages()
async def handler_message_deleted(client: Client, messages):
    """Обработка удаленных сообщений."""
    admins = [8140271247]
    print(messages[0]["_"])
    try:
        for message in messages:
            for admin in admins:
                try:
                    await client.send_message(
                        chat_id=admin,
                        text=f"""
🗑Менеджер удалил сообщение:

<u>Чат:</u>
id = <b>{message.chat.id}</b>
username = <b>{'@' + message.chat.username if message.chat.username else ''}</b>
name = <b>{message.chat.full_name}</b>

<u>Сообщение:</u>
id = <b>{message.chat.id}</b>


<u>Текст:</u>
{message.text}
""",
                        # дата отправки: <b>{message.date.strftime('%Y-%m-%d %H:%M:%S')}</b>
                        parse_mode=ParseMode.HTML,
                    )
                    logger.debug(f"Новое сообщение от {username}: {text}")
                except Exception as e:
                    logger.error(
                        f"Не удалось отправить уведомление админу {admin}: {e}"
                    )
    except Exception as e:
        logger.warning(f"Ошибка в обработчике удалённых сообщений: {e}")


@app.on_edited_message(filters.me)
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


# async def main():
#     while True:
#         try:
#             await app.start()
#
#         except Exception as e:
#             logger.exception("Main loop crashed, restarting in 5 sec")
#
#         finally:
#             try:
#                 await app.stop()
#             except:
#                 pass
#
#             await asyncio.sleep(5)


if __name__ == "__main__":
    app.run(use_qr=True)
