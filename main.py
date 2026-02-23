import asyncio

from loguru import logger

from src.config import user_bot, bot
from loguru import logger
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.enums import ParseMode
from pyrogram.types import ChatJoinRequest, Message, ChatMemberUpdated

from src.infra.databases.sql.uow import SQLAlchemyUnitOfWork
from src.presentation.telegram.mappers import (
    PyroMessageMapper,
    PyroChannelMapper,
    PyroUserMapper,
)
from src.infra.databases.sql.session import SessionFactory


@bot.on_chat_member_updated()
async def delete_channel(client: Client, event: ChatMemberUpdated):
    uow = SQLAlchemyUnitOfWork(session_factory=SessionFactory)
    me = event.new_chat_member.user.is_self
    status = event.new_chat_member.status
    if not me:
        return
    if status in ("left", "kicked"):
        async with uow:
            try:
                channel = await uow.channel_repo.get_by_id(event.chat.id)
                if channel is None:
                    channel = await uow.channel_repo.delete(event.chat.id)
                    logger.success("Successfully added a channel")
            except Exception as e:
                logger.error("An error ocured: {}", e)


@user_bot.on_message(filters.private & ~filters.bot, group=-1)
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


@user_bot.on_deleted_messages()
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


@user_bot.on_edited_message(filters.me)
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


@bot.on_chat_join_request(group=1)
async def new_members(client, message):
    logger.info(message)


@user_bot.on_chat_member_updated()
async def member_changed(client: Client, chat_member: ChatMemberUpdated):
    old = chat_member.old_chat_member
    new = chat_member.new_chat_member

    # пользователь ушёл
    if old.status in ["member", "restricted"] and new.status == "left":
        user = chat_member.from_user
        await client.send_message(chat_id=user.id, text="hello")

    # пользователь зашёл
    if old.status in ["left", "kicked"] and new.status in ["member", "restricted"]:
        user = chat_member.from_user
        await client.send_message(chat_id=user.id, text="goodbye")


async def main():
    await asyncio.gather(bot.start(), user_bot.start())

    print("Both clients started!")

    await asyncio.Event().wait()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
