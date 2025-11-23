from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from services import BookService
from dependencies.auth import get_current_user
from dependencies.db import get_db_session
from models import User
from schemas.book_schemas import BookResponse, BookCreate

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


@router.get("/{book_id}/")
async def get_book(
    book_id: int,
    curent_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    book_service = BookService(session)
    return await book_service.get_book(book_id)


@router.post("/", response_model=BookResponse)
async def create_book(
    book_data: BookCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    book_service = BookService(session)

    try:
        return await book_service.create_book(author_data.dict())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create book",
        )
