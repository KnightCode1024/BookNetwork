from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String

from db.models.base import Base


class User(Base):
    tg_id: Mapped[int] = mapped_column(
        BigInteger,
    )
    username: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    first_name: Mapped[str] = mapped_column(
        String,
    )
    last_name: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    user_books: Mapped[List["UserBook"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    collections: Mapped[List["Collection"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
