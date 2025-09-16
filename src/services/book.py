from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories.book import BookRepository
from db.models import Book, Genre, Author


class BookService:
    def __init__(self, session: AsyncSession):
        self.book_repository = BookRepository(session)

    async def add_book(
            self,
            book_title,
            book_dedcription,
            book_genre,
            book_year,
            author_first_name,
            author_last_name,
            author_patronymic,
    ):
        genre = Genre(name=book_genre)
        author = Author(
            first_name=author_first_name,
            last_name=author_last_name,
            patronymic=author_patronymic,
            )
        book = Book(
            name=book_title,
            description=book_dedcription,
            year=book_year,
            genre=genre,
            author=author,
                    )
        
        self.book_repository.add(book)
