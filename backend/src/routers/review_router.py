from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from services import ReviewService, LikeService
from dependencies.auth import get_current_user
from dependencies.db import get_db_session
from models import User
from schemas.review_schemas import (
    ReviewResponse,
    ReviewCreate,
    ReviewUpdate,
    ReviewDetailResponse,
    ReviewListResponse,
    ReviewStatsResponse,
)
from schemas.like_schemas import LikeResponse, LikeStatsResponse

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/", response_model=ReviewListResponse)
async def get_reviews(
    book_id: Optional[int] = Query(None, description="Filter by book ID"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    offset: int = Query(0, ge=0, description="Offset"),
    limit: int = Query(20, ge=1, le=100, description="Limit"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """Получить список отзывов с фильтрацией"""
    review_service = ReviewService(session)

    if book_id:
        reviews = await review_service.get_reviews_by_book_id(book_id, offset, limit)
        total = len(reviews)
    elif user_id:
        reviews = await review_service.get_reviews_by_user_id(user_id, offset, limit)
        total = len(reviews)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please specify either book_id or user_id filter",
        )

    return ReviewListResponse(
        items=reviews,
        total=total,
        offset=offset,
        limit=limit,
        has_more=(offset + limit) < total,
    )


@router.get("/{review_id}/", response_model=ReviewDetailResponse)
async def get_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    review_service = ReviewService(session)
    review = await review_service.get_review_by_id(review_id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )

    return review


@router.get("/book/{book_id}/stats/", response_model=ReviewStatsResponse)
async def get_book_review_stats(
    book_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    review_service = ReviewService(session)
    stats = await review_service.get_review_stats_by_book_id(book_id)

    from sqlalchemy import select, func
    from models import Review, ReviewStars

    rating_query = (
        select(Review.stars, func.count(Review.id).label("count"))
        .where(Review.book_id == book_id)
        .group_by(Review.stars)
    )

    result = await session.execute(rating_query)
    rating_distribution = {str(row[0].value): row[1] for row in result.all()}

    return ReviewStatsResponse(
        total_reviews=stats["total_reviews"],
        average_rating=stats["average_rating"],
        rating_distribution=rating_distribution,
        user_review_count=None,
    )


@router.post(
    "/", response_model=ReviewDetailResponse, status_code=status.HTTP_201_CREATED
)
async def create_review(
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    review_service = ReviewService(session)

    try:
        has_review = await review_service.user_has_review_for_book(
            current_user.id, review_data.book_id
        )

        if has_review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already reviewed this book",
            )

        review = await review_service.create_review(current_user.id, review_data.dict())

        full_review = await review_service.get_review_by_id(review.id)
        return full_review

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create review: {str(e)}",
        )


@router.patch("/{review_id}/", response_model=ReviewDetailResponse)
async def update_review_partial(
    review_id: int,
    review_data: ReviewUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    review_service = ReviewService(session)

    try:
        review = await review_service.update_review(
            review_id, current_user, review_data.dict(exclude_unset=True)
        )

        if not review:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this review or review not found",
            )
        full_review = await review_service.get_review_by_id(review_id)
        return full_review

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{review_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    review_service = ReviewService(session)

    success = await review_service.delete_review(review_id, current_user)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this review or review not found",
        )

    return None


@router.get("/user/me/", response_model=List[ReviewResponse])
async def get_my_reviews(
    offset: int = Query(0, ge=0, description="Offset"),
    limit: int = Query(20, ge=1, le=100, description="Limit"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    review_service = ReviewService(session)
    return await review_service.get_reviews_by_user_id(current_user.id, offset, limit)


@router.get("/book/{book_id}/my/", response_model=Optional[ReviewDetailResponse])
async def get_my_review_for_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    review_service = ReviewService(session)
    review = await review_service.get_user_review_for_book(current_user.id, book_id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You haven't reviewed this book yet",
        )

    return await review_service.get_review_by_id(review.id)


@router.post(
    "/{review_id}/like/",
    response_model=LikeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def like_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    like_service = LikeService(session)

    review_service = ReviewService(session)
    review = await review_service.get_review_by_id(review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )

    already_liked = await like_service.check_user_liked(current_user.id, review_id)
    if already_liked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already liked this review",
        )

    if review.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot like your own review",
        )

    like = await like_service.like_review(current_user.id, review_id)
    if not like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to like review"
        )

    return like


@router.delete("/{review_id}/like/", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    like_service = LikeService(session)

    review_service = ReviewService(session)
    review = await review_service.get_review_by_id(review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )

    already_liked = await like_service.check_user_liked(current_user.id, review_id)
    if not already_liked:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You haven't liked this review yet",
        )

    success = await like_service.unlike_review(current_user.id, review_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to unlike review"
        )

    return None


@router.get("/{review_id}/likes/", response_model=List[LikeResponse])
async def get_review_likes(
    review_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    like_service = LikeService(session)

    review_service = ReviewService(session)
    review = await review_service.get_review_by_id(review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )

    likes = await like_service.get_user_likes(current_user.id)

    review_likes = [like for like in likes if like.review_id == review_id]

    return review_likes


@router.get("/{review_id}/likes/count/", response_model=Dict[str, Any])
async def get_review_likes_count(
    review_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    like_service = LikeService(session)

    review_service = ReviewService(session)
    review = await review_service.get_review_by_id(review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )

    stats = await like_service.get_review_likes_stats(review_id)

    return {
        "review_id": review_id,
        "likes_count": stats["likes_count"],
        "has_likes": stats["likes_count"] > 0,
    }


@router.get("/{review_id}/likes/stats/", response_model=LikeStatsResponse)
async def get_review_likes_stats_with_user(
    review_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    like_service = LikeService(session)

    review_service = ReviewService(session)
    review = await review_service.get_review_by_id(review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )

    stats = await like_service.get_review_likes_stats(review_id, current_user.id)

    return LikeStatsResponse(
        review_id=review_id,
        like_count=stats["likes_count"],
        user_liked=stats.get("user_liked", False),
    )


@router.get("/{review_id}/likes/check/", response_model=Dict[str, bool])
async def check_if_user_liked_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    like_service = LikeService(session)

    review_service = ReviewService(session)
    review = await review_service.get_review_by_id(review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )

    liked = await like_service.check_user_liked(current_user.id, review_id)

    return {"liked": liked, "review_id": review_id, "user_id": current_user.id}
