from pyrogram.client import Client
from src.user_bot import handlers, fetch_missing_messages, polling_chat_request


class UserBot:
    def __init__(
        self,
        client: Client,
        check_missing_messages: bool = False,
        check_join_request: bool = False,
    ):
        self.client = client
        self.check_missing_messages = check_missing_messages
        self.check_join_request = check_join_request
        for handler in handlers:
            self.client.add_handler(handler)

    async def start(self):
        if self.check_missing_messages:
            await fetch_missing_messages(self.client)
        if self.check_join_request:
            await polling_chat_request(self.client)
