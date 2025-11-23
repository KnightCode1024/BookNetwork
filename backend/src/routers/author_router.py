from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.auth import get_current_user
from dependencies.db import get_db_session
from models import User
from schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse
from services import AuthorService

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("/{author_id}/", response_model=AuthorResponse)
async def get_author_by_id(
    author_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    author_service = AuthorService(session)
    author = await author_service.get_author_by_id(author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )
    return author


@router.get("/", response_model=List[AuthorResponse])
async def get_all_authors(
    offset: int = Query(0, ge=0, description="Offset"),
    limit: int = Query(20, ge=1, le=100, description="Limit"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    author_service = AuthorService(session)
    return await author_service.get_all_authors(offset, limit)


@router.get("/search/", response_model=List[AuthorResponse])
async def search_authors(
    query: str = Query(..., min_length=1, description="Search term"),
    limit: int = Query(20, ge=1, le=50, description="Limit"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    author_service = AuthorService(session)
    return await author_service.search_authors(query, limit)


@router.get("/by-name/", response_model=Optional[AuthorResponse])
async def get_author_by_name(
    name: str = Query(..., description="Author name"),
    surname: str = Query(..., description="Author surname"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    author_service = AuthorService(session)
    author = await author_service.get_author_by_name(name, surname)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )
    return author


@router.post("/", response_model=AuthorResponse)
async def create_author(
    author_data: AuthorCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    author_service = AuthorService(session)

    try:
        return await author_service.create_author(author_data.dict())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create author",
        )


@router.delete("/{author_id}/")
async def delete_author(
    author_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    author_service = AuthorService(session)
    success = await author_service.delete_author(author_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found",
        )
    return {"message": "Author deleted successfully"}


@router.patch("/{author_id}/", response_model=AuthorResponse)
async def partial_update_author(
    author_id: int,
    author_data: AuthorUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    author_service = AuthorService(session)

    try:
        author = await author_service.partial_update_author(
            author_id, author_data.dict(exclude_unset=True)
        )
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
            )
        return author
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{author_id}/", response_model=AuthorResponse)
async def update_author(
    author_id: int,
    author_data: AuthorUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    author_service = AuthorService(session)

    try:
        author = await author_service.update_author(author_id, author_data.dict())
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
            )
        return author
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
