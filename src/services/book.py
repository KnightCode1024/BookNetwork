from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories.book import BookRepository


class BookService:
    def __init__(self, session: AsyncSession):
        self.user_repository = BookRepository(session)
