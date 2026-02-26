import asyncio

from loguru import logger
from datetime import datetime, timedelta
from pyrogram.client import Client
from pyrogram.types import ChatJoinRequest, ChatMemberUpdated, ChatJoiner

from conf import HELLO_MSG, GOODBYE_MSG, CHANNEL
from src.database.repositories import MessageRepository, UserRepository
from src.database.models import Message, User
from src.database.session import SessionFactory
from src.database.exceptions import UserNotFoundError


async def polling_chat_request(client: Client):
    message_repo = MessageRepository(session=SessionFactory)  # type: ignore
    user_repo = UserRepository(session=SessionFactory)
    chat = await client.get_chat("https://t.me/+kP0wf8XdpXwxZjY6")
    # chat = await client.get_chat("https://t.me/+jCX3RyK5zMRjOGMy")
    while True:
        try:
            async for request in client.get_chat_join_requests(chat.id):  # type: ignore
                try:
                    if not isinstance(request, ChatJoiner):
                        continue

                    now_dt = datetime.now()
                    if (now_dt - request.date) > timedelta(minutes=10):
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


async def new_member(
    client: Client,
    join_request: ChatJoinRequest,
):
    if join_request.chat.id == CHANNEL:
        await join_request.approve()
        await client.send_message(chat_id=join_request.from_user.id, text=HELLO_MSG)
        logger.info(
            f"Юзер {join_request.from_user.id} присоеденился в канал: {join_request.chat.id}"
        )


async def member_changed(client: Client, chat_member: ChatMemberUpdated):
    if chat_member.old_chat_member:
        await client.send_message(
            chat_id=chat_member.old_chat_member.user.id, text=GOODBYE_MSG
        )
