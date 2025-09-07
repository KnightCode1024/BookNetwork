from sqlalchemy.ext.asyncio import AsyncSession

from db.models.genre import Genre
from db.repositories.base import BaseRepository


class GenreRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Genre)
