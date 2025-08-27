from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from db.models.base import Base
from db.models.association import books_genres


class Book(Base):
    name: Mapped[str] = mapped_column(
        String,
    )
    description: Mapped[str] = mapped_column(
        String,
    )
    year: Mapped[str] = mapped_column(
        String,
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
    user_book: Mapped["UserBook"] = relationship(
        back_populates="books",
    )
