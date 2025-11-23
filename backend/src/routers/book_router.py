from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from services import BookService
from dependencies.auth import get_current_user
from dependencies.db import get_db_session
from models import User

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/")
async def get_books(
    offset: int = Query(0, ge=0, description="Offset"),
    limit: int = Query(20, ge=1, le=100, description="Limit"),
    curent_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    book_service = BookService(session)
    return await book_service.get_books(offset, limit)



