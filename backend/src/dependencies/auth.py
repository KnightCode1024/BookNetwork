from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from dependencies.db import get_db_session
from services.user_service import UserService

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPBearer = Depends(security),
    session: AsyncSession = Depends(get_db_session),
):
    user_service = UserService(session)
    user = await user_service.verify_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return user
