from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text

from db.models.base import Base
from db.enums.status_enum import StatusEnum
from db.enums.rating_enum import RatingEnum


class UserBook(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
    )
    status: Mapped[StatusEnum]
    rating: Mapped[RatingEnum]
    review: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    user: Mapped["User"] = relationship(
        back_populates="user_books",
    )

    book: Mapped["Book"] = relationship(
        back_populates="user_books",
    )
