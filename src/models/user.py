from typing import List

from sqlalchemy.orm import Mapped, mapped_column
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import relationship
from sqlalchemy import String
from pydantic import validator

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

    otp_sessions: Mapped[List["OTPSession"]] = relationship(
        "OTPSession",
         back_populates="user",
         )

    
    @validator('email')
    def validate_email_format(cls, v):
        if not v:
            raise ValueError('Email cannot be empty')
        
        try:
            valid = validate_email(v, check_deliverability=False)
            return valid.email.lower()
        except EmailNotValidError as e:
            raise ValueError(f'Invalid email format: {str(e)}')
    