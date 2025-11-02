from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.auth import UserSchema, TokenInfo, LoginSchema
from dependencies.auth import validate_auth_user
from utils import auth_utils
from dependencies.db import get_db_session
from services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["AUTH"])

@router.post("/login/", response_model=TokenInfo)
async def auth_user(
    user_data: LoginSchema,
    session: AsyncSession = Depends(get_db_session),
):
    user_service = UserService(session)

    password_str = user_data.password
    if isinstance(password_str, bytes):
        password_str = password_str.decode("utf-8")

    token = await user_service.login_user(
        username=user_data.username,
        password=password_str,
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )