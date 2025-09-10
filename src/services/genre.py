import pickle

import redis
from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories.genre import GenreRepository
from config.config import settings


class GenreService:
    def __init__(self, session: AsyncSession):
        self.genre_repository = GenreRepository(session)

    async def get_all_genres(self):
        print("Вызов функции для получения всех жанров")
        redis_client = redis.Redis(host=settings.redis.HOST)
        cache_genres = redis_client.get("book_genres")

        if cache_genres is not None:
            print("Отдайм данные из редиски")
            return pickle.loads(cache_genres)
        
        result = await self.genre_repository.get_all()
        redis_client.set("book_genres", pickle.dumps(result), ex=1800)
        print("Отдаём данные из БД")
        return result
