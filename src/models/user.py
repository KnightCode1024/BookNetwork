from typing import List

from sqlalchemy.orm import Mapped, mapped_column
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import relationship, validates
from sqlalchemy import String

from models import Base


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
    
    @validates('email')
    def validate_email_format(self, key, email):
        if not email:
            raise ValueError('Email cannot be empty')
        
        from email_validator import validate_email, EmailNotValidError
        try:
            valid = validate_email(email, check_deliverability=False)
            return valid.email.lower()
        except EmailNotValidError as e:
            raise ValueError(f'Invalid email format: {str(e)}')
    