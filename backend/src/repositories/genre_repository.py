from sqlalchemy.ext.asyncio import AsyncSession

from repositories import BaseRepository
from models import Genre


class GenreRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Genre, session)
