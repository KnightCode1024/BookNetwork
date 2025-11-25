from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from services import BookService
from dependencies.auth import get_current_user
from dependencies.db import get_db_session
from models import User
from schemas.book_schemas import BookResponse, BookCreate, BookUpdate

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


@router.delete("/{book_id}/")
async def delete_book(
    book_id: int,
    curent_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    book_service = BookService(session)
    success = await book_service.delete_book(book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return {"message": "Book deleted successfully"}


@router.patch("/{book_id}/", response_model=BookResponse)
async def update_book_partial(
    book_id: int,
    book_data: BookUpdate,
    curent_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    book_service = BookService(session)
    try:
        book = await book_service.partial_update_book(
            book_id, book_data.dict(exclude_unset=True)
        )
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
        return book
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



@router.put("/{book_id}/", response_model=BookResponse)
async def update_book(
    book_id: int,
    book_data: BookUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    book_service = BookService(session)

    try:
        book = await book_service.update_book(book_id, book_data.dict())
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )
        return book
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

