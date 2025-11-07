from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db import get_db_session
from services.user_service import UserService

async def get_current_user(
    token: str,
    session: AsyncSession = Depends(get_db_session),
):
    user_service = UserService(session)
    user = await user_service.verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return user
