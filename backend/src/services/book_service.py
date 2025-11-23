from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models import Book
from repositories import BookRepository


class BookService:
    def __init__(self, session: AsyncSession):
        self.book_repo = BookRepository(session)

    async def get_books(self, offset: int = 0, limit: int = 20):
        return await self.book_repo.get_books_by_id_with_author_and_genre(offset, limit)

    async def get_book_by_id(self, book_id: int):
        return await self.book_repo.get_book_by_id(book_id)

    async def create_book(self, book_data: dict) -> Book:
        return await self.book_repo.create(book_data)

    async def update_book(self, book_id: int, book_data: dict) -> Optional[Book]:
        return await self.book_repo.update(book_id, book_data)

    async def delete_book(self, book_id: int) -> bool:
        return await self.book_repo.delete(book_id)
