from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Boolean, ForeignKey

from db.models.base import Base


class Collection(Base):
    name: Mapped[str] = mapped_column(
        String,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    is_public: Mapped[bool] = mapped_column(
        Boolean,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    user: Mapped["User"] = relationship(
        back_populates="collections",
    )
