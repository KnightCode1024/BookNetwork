from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from db.models.base import Base


class Author(Base):
    first_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    patronymic: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    books: Mapped[List["Book"]] = relationship(
        "Book",
        back_populates="author",
    )
