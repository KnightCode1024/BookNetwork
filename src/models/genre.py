from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, ForeignKey, DateTime

from models import Base


class Genre(Base):
    name: Mapped[str] = mapped_column(String())
