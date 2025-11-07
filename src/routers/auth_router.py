from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.auth import TokenPair, LoginSchema, UserSchema, RefreshTokenSchema
from dependencies.db import get_db_session
from services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["AUTH"])

@router.post("/login/", response_model=TokenPair)
async def auth_user(
    user_data: LoginSchema,
    session: AsyncSession = Depends(get_db_session),
):
    user_service = UserService(session)

    tokens = await user_service.login_user(
        username=user_data.username,
        password=user_data.password,
    )

    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    access_token, refresh_token = tokens
    
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
    )

@router.post("/register/", response_model=TokenPair)
async def register_user(
    user_data: UserSchema,
    session: AsyncSession = Depends(get_db_session),
):
    user_service = UserService(session)

    try:
        user = await user_service.create_user({
            "username": user_data.username,
            "email": user_data.email,
            "password": user_data.password
        })
        
        tokens = await user_service.login_user(
            username=user_data.username,
            password=user_data.password,
        )
        
        if not tokens:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate tokens",
            )
        
        access_token, refresh_token = tokens
        
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.post("/refresh/", response_model=TokenPair)
async def refresh_tokens(
    token_data: RefreshTokenSchema,
    session: AsyncSession = Depends(get_db_session),
):
    user_service = UserService(session)

    tokens = await user_service.refresh_tokens(token_data.refresh_token)

    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    
    access_token, refresh_token = tokens
    
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
    )

@router.post("/verify/")
async def verify_token(
    token_data: RefreshTokenSchema, 
    session: AsyncSession = Depends(get_db_session),
):
    user_service = UserService(session)

    user = await user_service.verify_token(token_data.refresh_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    
    return {
        "valid": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }