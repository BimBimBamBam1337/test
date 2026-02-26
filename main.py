import asyncio
from pyrogram import Client, idle
from loguru import logger

from src.config import bot_client, user_bot_client
from src.bot.bot import Bot
from src.user_bot.user_bot import UserBot


async def main():
    bot = Bot(bot_client, check_join_request=True)
    user_bot = UserBot(user_bot_client, check_missing_messages=True)

    await bot.client.start()
    await user_bot.client.start()

    logger.info("Clients started")

    await idle()

    await bot.client.stop()
    await user_bot.client.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
