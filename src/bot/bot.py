from pyrogram.client import Client
from src.bot import handlers


class Bot:
    def __init__(
        self,
        client: Client,
    ):
        self.client = client

        for handler in handlers:
            self.client.add_handler(handler)
