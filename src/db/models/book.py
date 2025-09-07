from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer

from db.models.base import Base
from db.models.association import books_genres


class Book(Base):
    name: Mapped[str] = mapped_column(
        String,
    )
    description: Mapped[str] = mapped_column(
        String,
    )
    year: Mapped[int] = mapped_column(
        Integer,
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id"),
    )
    author: Mapped["Author"] = relationship(
        "Author",
        back_populates="books",
    )
    genres: Mapped[List["Genre"]] = relationship(
        "Genre",
        secondary=books_genres,
        back_populates="books",
    )
    user_books: Mapped[List["UserBook"]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
    )
