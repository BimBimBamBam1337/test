from loguru import logger
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import ChatMemberUpdated

from config import app
from domain.entities import Channel
from infra.databases.sql.uow import SQLAlchemyUnitOfWork
from presentation.telegram import texts


@app.on_chat_member_updated()
async def registre_channel(
    client: Client, event: ChatMemberUpdated, uow: SQLAlchemyUnitOfWork
):
    if event.new_chat_member and event.new_chat_member.user.is_self:
        async with uow:
            try:
                channel = await uow.channel_repo.get_by_id(event.chat.id)
                if channel is None:
                    channel = await uow.channel_repo.create(event.chat.id)
                    logger.success("Successfully added a channel")
            except Exception as e:
                logger.error("An error ocured: {}", e)


@app.on_chat_member_updated()
async def delete_channel(
    client: Client, event: ChatMemberUpdated, uow: SQLAlchemyUnitOfWork
):
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
