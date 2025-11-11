from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, ForeignKey, DateTime

from models import Base

class Book(Base):
    title: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(Text())
    publication_year: Mapped[datetime] = mapped_column(DateTime())

    author_id: Mapped[int] = mapped_column(
        ForeignKey(
            "authors.id", 
            ondelete="CASCADE",
            ),
        index=True,
    )