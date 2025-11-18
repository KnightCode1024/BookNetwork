from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, DateTime, Integer

from models import Base


class Book(Base):
    title: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(Text())
    publication_year: Mapped[int] = mapped_column(Integer())

    author_id: Mapped[int] = mapped_column(
        ForeignKey(
            "authors.id",
            ondelete="CASCADE",
        ),
        index=True,
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey(
            "genres.id",
            ondelete="CASCADE",
        )
    )

    author: Mapped["Author"] = relationship("Author", back_populates="books")
    genre: Mapped["Genre"] = relationship("Genre", back_populates="books")
