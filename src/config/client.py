from conf import *
from pyrogram.client import Client
from src.constants import SESSIONS_DIR


def create_user():
    return Client(
        name="news_poster_bot",  # только имя
        api_id=API_ID,
        api_hash=API_HASH,
        phone_number=PHONE,
        workdir=SESSIONS_DIR,  # папка отдельно
    )


def create_bot():
    return Client(
        name="my_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=TOKEN,
        workdir=SESSIONS_DIR,
    )
