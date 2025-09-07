from sqlalchemy.ext.asyncio import AsyncSession

from db.models.book import Book
from db.repositories.base import BaseRepository


class BookRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Book)

    async def add_book():
        pass
