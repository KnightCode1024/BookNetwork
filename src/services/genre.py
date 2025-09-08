from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories.genre import GenreRepository


class GenreService:
    def __init__(self, session: AsyncSession):
        self.genre_repository = GenreRepository(session)

    async def get_all_genres(self):
        return await self.genre_repository.get_all()
