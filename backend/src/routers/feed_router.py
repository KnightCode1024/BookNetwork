from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from services import FeedService
from dependencies.db import get_db_session
from schemas.feed_schemas import FeedResponse, FeedFilters

router = APIRouter(prefix="/feed", tags=["Feed"])


@router.get("/", response_model=FeedResponse)
async def get_feed(
    offset: int = Query(0, ge=0, description="Offset"),
    limit: int = Query(20, ge=1, le=100, description="Limit"),
    book_id: Optional[int] = Query(None, description="Filter by book ID"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    genre_id: Optional[int] = Query(None, description="Filter by genre ID"),
    author_id: Optional[int] = Query(None, description="Filter by author ID"),
    min_stars: Optional[int] = Query(None, ge=1, le=5, description="Minimum stars"),
    max_stars: Optional[int] = Query(None, ge=1, le=5, description="Maximum stars"),
    order_by: Optional[str] = Query(
        "newest", 
        description="Order by: newest, oldest, highest_rated"
    ),
    session: AsyncSession = Depends(get_db_session),
):  
    feed_service = FeedService(session)
    
    filters = FeedFilters(
        book_id=book_id,
        user_id=user_id,
        genre_id=genre_id,
        author_id=author_id,
        min_stars=min_stars,
        max_stars=max_stars,
        order_by=order_by,
    ).dict(exclude_none=True)
    
    return await feed_service.get_feed(offset, limit, filters)


@router.get("/recent/", response_model=FeedResponse)
async def get_recent_feed(
    days: int = Query(7, ge=1, le=30, description="Days to consider"),
    limit: int = Query(10, ge=1, le=50, description="Limit"),
    session: AsyncSession = Depends(get_db_session),
):    
    feed_service = FeedService(session)
    reviews = await feed_service.get_recent_activity(days, limit)
    
    return FeedResponse(
        reviews=reviews,
        total=len(reviews),
        offset=0,
        limit=limit,
        has_more=False
    )
