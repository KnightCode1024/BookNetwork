from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models import Genre


from repositories import GenreRepository


class GenreService:
    def __init__(self, session: AsyncSession):
        self.genre_repo = GenreRepository(session)

    async def get_all_genres(self, offset: int = 0, limit: int = 20) -> List[Genre]:
        return await self.genre_repo.get_all(offset, limit)

    async def get_genre_by_id(self, genre_id: int):
        return await self.genre_repo.get_by_id(genre_id)

    async def create_genre(self, genre_data: dict) -> Genre:
        return await self.genre_repo.create(genre_data)

    async def delete_genre(self, genre_id: int) -> bool: 
        return await self.genre_repo.delete(genre_id)

    async def partial_update_genre(self, genre_id: int, genre_data: dict) -> Optional[Author]:
        update_data = {k: v for k, v in genre_data.items() if v is not None}
        self._validate_dates(update_data)
        return await self.genre_repo.update(genre_id, update_data)
