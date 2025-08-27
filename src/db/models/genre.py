from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from db.models.base import Base
from db.models.association import books_genres


class Genre(Base):
    name: Mapped[str] = mapped_column(
        String,
    )

    books: Mapped[List["Book"]] = relationship(
        "Book",
        secondary=books_genres,
        back_populates="genres",
    )
