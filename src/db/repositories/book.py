from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Book

from db.repositories.base import BaseRepository


class BookRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Book)

        
