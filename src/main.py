import asyncio
import logging
from aiogram import Bot, Dispatcher

from config.config import settings
from handlers.handlers import router


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.bot.TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        router,
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
