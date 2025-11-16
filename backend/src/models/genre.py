from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, DateTime

from models import Base


class Genre(Base):
    name: Mapped[str] = mapped_column(String())

    books: Mapped[List["Book"]] = relationship("Book", back_populates="genre")
