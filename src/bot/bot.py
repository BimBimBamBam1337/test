from pyrogram.client import Client
from src.bot import handlers, polling_chat_request


class Bot:
    def __init__(
        self,
        client: Client,
        check_join_request: bool = False,
    ):
        self.client = client
        self.check_join_request = check_join_request
        for handler in handlers:
            self.client.add_handler(handler)

    async def start(self):
        if self.check_join_request:
            await polling_chat_request(self.client)
