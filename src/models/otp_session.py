from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey

from models import Base


class OTPSession(Base):
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    otp_code: Mapped[str] = mapped_column(
        String(6), 
        nullable=False,
        )
    secret: Mapped[str] = mapped_column(
        String(32), 
        nullable=False,
        ) 
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False,
        ) 
    is_used: Mapped[bool] = mapped_column(
        Boolean, 
        default=False,
        )
    purpose: Mapped[str] = mapped_column(
        String(20),
        )  # 'login', 'registration', 'password_reset'
    
    user = relationship("User", back_populates="otp_sessions")