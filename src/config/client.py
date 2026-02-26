from conf import *
from pyrogram.client import Client
from src.constants import SESSIONS_DIR

user_bot_client = Client(
    name="news_poster_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    phone_number=PHONE,
    workdir=SESSIONS_DIR,
)


bot_client = Client(
    name="my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    workdir=SESSIONS_DIR,
)
