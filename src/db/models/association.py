from sqlalchemy import Table, Column, ForeignKey, Integer

from db.models.base import Base


books_genres = Table(
    "books_genres",
    Base.metadata,
    Column(
        "book_id",
        Integer,
        ForeignKey("books.id"),
        primary_key=True,
    ),
    Column(
        "genre_id",
        Integer,
        ForeignKey("genres.id"),
        primary_key=True,
    ),
)
