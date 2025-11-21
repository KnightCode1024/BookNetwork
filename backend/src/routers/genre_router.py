from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services.genre_service import GenreService
from dependencies.db import get_db_session
from dependencies.auth import get_current_user
from schemas.genre import CreateGenre, GenreResponse, GenreUpdate
from models import User

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.get("/")
async def get_all_genres(
    offset: int = Query(0, ge=0, description="Offset"),
    limit: int = Query(20, ge=1, le=100, description="Limit"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    genre_service = GenreService(session)
    return await genre_service.get_all_genres(offset, limit)


@router.get("/{genre_id}/")
async def get_genre_by_id(
    genre_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    genre_service = GenreService(session)
    return await genre_service.get_genre_by_id(genre_id)


@router.post("/", response_model=GenreResponse)
async def add_genre(
    genre_data: CreateGenre,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    genre_service = GenreService(session)
    try:
        return await genre_service.create_genre(genre_data.dict())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create genre",
        )


@router.delete("/{genre_id}/")
async def delete_genre(
    genre_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
):
    genre_service = GenreService(session)
    success = await genre_service.delete_genre(genre_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found",
        )
    return {"message": "Genre deleted successfully"}


@router.patch("/{genre_id}")
async def update_genre(
    author_id: int,
    genre_data: GenreUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    genre_service = GenreService(session)

    try:
        genre = await genre_service.partial_update_genre(
            genre_id, genre_data.dict(exclude_unset=True),
        )

        if not genre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found",)
        return genre
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
