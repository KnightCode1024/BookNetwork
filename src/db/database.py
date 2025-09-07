from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)
from config.config import settings

DATABASE_URL = settings.database.get_db_url()
DEBUG = settings.bot.DEBUG

echo = False
if DEBUG:
    echo = True


engine = create_async_engine(
    url=DATABASE_URL,
    echo=echo,
)
async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncSession:
    return async_session_maker()
