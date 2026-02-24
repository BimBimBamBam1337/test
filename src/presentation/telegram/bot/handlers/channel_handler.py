from loguru import logger

from loguru import logger
from pyrogram.client import Client
from pyrogram.types import ChatJoinRequest, ChatMemberUpdated

from src.infra.databases.sql.uow import SQLAlchemyUnitOfWork
from src.presentation.telegram.mappers import (
    PyroChannelMapper,
)
from src.infra.databases.sql.session import SessionFactory

async def new_member(client:Client, join_request:ChatJoinRequest)
    logger.info(join_request)

async def member_changed(client: Client, chat_member: ChatMemberUpdated):
    old = chat_member.old_chat_member
    new = chat_member.new_chat_member
    if new:
        user = chat_member.from_user
        await client.send_message(chat_id=user.id, text="hello")

    if old:
        user = chat_member.from_user
        await client.send_message(chat_id=user.id, text="goodbye")
