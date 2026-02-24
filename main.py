import asyncio

from loguru import logger

from src.config import user_bot, bot


async def main():
    await asyncio.gather(bot.start(), user_bot.start())

    logger.info("Both clients started!")

    await asyncio.Event().wait()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
