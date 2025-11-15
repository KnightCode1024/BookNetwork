from enum import Enum
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from email_validator import validate_email, EmailNotValidError
from sqlalchemy import String, Enum as SQLEnum


from models import Base


class MyUserRole(Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

class User(Base):
    username: Mapped[str] = mapped_column(
        String(255),
        nullable=False, 
        unique=True,
        index=True,
        )
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False, 
        unique=True,
        index=True,
        )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
    )
    role: Mapped[MyUserRole] = mapped_column(
        SQLEnum(MyUserRole), 
        nullable=False,
        default=MyUserRole.USER,
    )
    
    @validates('email')
    def validate_email_format(self, key, email):
        if not email:
            raise ValueError('Email cannot be empty')
        
        try:
            valid = validate_email(email, check_deliverability=False)
            return valid.email.lower()
        except EmailNotValidError as e:
            raise ValueError(f'Invalid email format: {str(e)}')
    