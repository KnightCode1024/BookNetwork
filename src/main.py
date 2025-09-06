import asyncio
import logging
from aiogram import Bot, Dispatcher

from core.config import settings
from handlers.users import router as user_router


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.bot.TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        user_router,
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
