from datetime import datetime

from sqlalchemy import String, DateTime, Text
from  sqlalchemy.orm import Mapped, mapped_column

from models import Base

class Author(Base):
    name: Mapped[str] = mapped_column(String())
    surname: Mapped[str] = mapped_column(String())
    patranymic: Mapped[str] = mapped_column(String())
    bio: Mapped[str] = mapped_column(Text())
    date_birth: Mapped[datetime] = mapped_column(DateTime())
    date_death: Mapped[datetime] = mapped_column(DateTime())