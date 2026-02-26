from pyrogram.handlers.chat_join_request_handler import ChatJoinRequestHandler
from pyrogram.handlers.chat_member_updated_handler import ChatMemberUpdatedHandler

from .handlers import new_member, member_changed

handlers = [
    # ChatJoinRequestHandler(new_member),
    ChatMemberUpdatedHandler(member_changed),
]
