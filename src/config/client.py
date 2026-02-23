from pyrogram.client import Client
from .settings import settings
from src.constants import SESSIONS_DIR

# name= {SESSIONS_DIR}/
user_bot = Client(
    name=f"{SESSIONS_DIR}/news_poster_bot",
    api_hash=settings.api_hash,
    api_id=settings.api_id,
    phone_number=settings.phone,
    workdir=f"{SESSIONS_DIR}",
)
bot = Client(
    name=f"{SESSIONS_DIR}/my_bot",
    api_id=settings.api_id,
    api_hash=settings.api_hash,
    bot_token=settings.token,
)
