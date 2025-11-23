from typing import List
from datetime import datetime

from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class Author(Base):
    name: Mapped[str] = mapped_column(String())
    surname: Mapped[str] = mapped_column(String())
    patronymic: Mapped[str] = mapped_column(String())
    bio: Mapped[str] = mapped_column(Text())
    date_birth: Mapped[datetime] = mapped_column(DateTime())
    date_death: Mapped[datetime] = mapped_column(DateTime())

    books: Mapped[List["Book"]] = relationship("Book", back_populates="author")

    def __str__(self):
        return f"{self.name[0].upper()}.{self.patronymic[0].upper()}.{self.surname.capitalize()}"
