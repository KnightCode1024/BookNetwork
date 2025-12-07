from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from models import Base


class Like(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    review_id: Mapped[int] = mapped_column(
        ForeignKey("reviews.id", ondelete="CASCADE"),
        primary_key=True,
    )

    review: Mapped["Review"] = relationship(
        "Review",
        back_populates="likes",
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="likes",
    )
