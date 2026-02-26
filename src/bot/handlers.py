import asyncio

from loguru import logger
from datetime import datetime, timedelta
from pyrogram.client import Client
from pyrogram.types import ChatJoinRequest, ChatMemberUpdated, ChatJoiner

from conf import HELLO_MSG, GOODBYE_MSG, CHANNEL
from src.config import user_bot_client


async def new_member(
    client: Client,
    join_request: ChatJoinRequest,
):
    if join_request.chat.id == CHANNEL:
        await join_request.approve()
        await user_bot_client.send_message(
            chat_id=join_request.from_user.id, text=HELLO_MSG
        )
        logger.info(
            f"Юзер {join_request.from_user.id} присоеденился в канал: {join_request.chat.id}"
        )


async def member_changed(client: Client, chat_member: ChatMemberUpdated):
    if chat_member.old_chat_member:
        await user_bot_client.send_message(
            chat_id=chat_member.old_chat_member.user.id, text=GOODBYE_MSG
        )
