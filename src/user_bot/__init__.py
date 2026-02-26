from pyrogram import filters
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.handlers.deleted_messages_handler import DeletedMessagesHandler
from pyrogram.handlers.edited_message_handler import EditedMessageHandler

from .handlers import (
    handler_new_message,
    handler_message_edited,
    handler_message_deleted,
    fetch_missing_messages,
    polling_chat_request,
)

handlers = [
    MessageHandler(handler_new_message, filters.private & ~filters.bot),
    EditedMessageHandler(handler_message_edited, filters.private & ~filters.bot),
    DeletedMessagesHandler(handler_message_deleted),
]
