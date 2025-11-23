from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from models import Book
from repositories import BaseRepository


class BookRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Book, session)

    async def get_books_by_id_with_author_and_genre(
        self,
        offset: int = 0,
        limit: int = 20,
    ):
        query = (
            select(self.model)
            .offset(offset)
            .limit(limit)
            .options(selectinload(self.model.author))
            .options(selectinload(self.model.genre))
        )
        result = await self.session.execute(query)
        return result.unique().scalars().all()

    async def get_book_by_id(self, book_id: int):
        query = (
            select(self.model)
            .where(self.model.id == book_id)
            .options(selectinload(self.model.author))
            .options(selectinload(self.model.genre))
        )
        result = await self.session.execute(query)
        return result.unique.scalar_one_or_none()
