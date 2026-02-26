from pyrogram.client import Client
from src.user_bot import handlers, fetch_missing_messages


class UserBot:
    def __init__(
        self,
        client: Client,
        check_missing_messages: bool = False,
    ):
        self.client = client
        self.check_missing_messages = check_missing_messages
        for handler in handlers:
            self.client.add_handler(handler)

    async def start(self):
        if self.check_missing_messages:
            await fetch_missing_messages(self.client)
