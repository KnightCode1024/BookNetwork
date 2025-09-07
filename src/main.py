import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis


from config.config import settings
from handlers.user import router as user_router
from handlers.book import router as book_router


async def main():
    if settings.bot.DEBUG:
        logging.basicConfig(level=logging.INFO)

    redis = Redis(host=settings.redis.HOST)
    storage = RedisStorage(redis=redis)

    bot = Bot(token=settings.bot.TOKEN)
    dp = Dispatcher(storage=storage)

    dp.include_routers(
        user_router,
        book_router,
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
