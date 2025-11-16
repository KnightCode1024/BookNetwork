from enum import IntEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from models import Base


class ReviewStars(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class Review(Base):
    title: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )
    stars: Mapped[ReviewStars] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        index=True,
    )
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship("User", back_populates="reviews")
    book: Mapped["Book"] = relationship("Book")
