# feed_repository.py - исправленная версия
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, desc, asc
from sqlalchemy.orm import joinedload

from models import Review, Book, Author, Genre, User, Like


class FeedRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_feed(
        self, offset: int = 0, limit: int = 20, filters: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[Review, int]]:
        likes_subquery = (
            select(Like.review_id, func.count(Like.review_id).label("likes_count"))
            .group_by(Like.review_id)
            .subquery()
        )

        query = (
            select(
                Review,
                func.coalesce(likes_subquery.c.likes_count, 0).label("likes_count"),
            )
            .join(Review.user)
            .join(Review.book)
            .join(Book.author)
            .join(Book.genre)
            .outerjoin(likes_subquery, likes_subquery.c.review_id == Review.id)
            .options(
                joinedload(Review.user),
                joinedload(Review.book).joinedload(Book.author),
                joinedload(Review.book).joinedload(Book.genre),
            )
        )

        if filters:
            query = self._apply_filters(query, filters)

        query = self._apply_ordering(
            query, filters.get("order_by") if filters else "newest"
        )

        query = query.offset(offset).limit(limit)

        result = await self.session.execute(query)
        return result.all()

    async def get_feed_with_stats(
        self, offset: int = 0, limit: int = 20, filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        review_tuples = await self.get_feed(offset, limit, filters)
        reviews_with_likes = []
        for review, likes_count in review_tuples:
            review.likes_count = likes_count
            reviews_with_likes.append(review)

        count_query = select(func.count(Review.id))
        if filters:
            count_query = self._apply_filters(count_query, filters)

        result = await self.session.execute(count_query)
        total = result.scalar()

        return {
            "reviews": reviews_with_likes,
            "total": total,
            "offset": offset,
            "limit": limit,
            "has_more": (offset + limit) < total,
        }

    def _apply_filters(self, query, filters: Dict[str, Any]):
        conditions = []

        if book_id := filters.get("book_id"):
            conditions.append(Review.book_id == book_id)

        if user_id := filters.get("user_id"):
            conditions.append(Review.user_id == user_id)

        if genre_id := filters.get("genre_id"):
            conditions.append(Book.genre_id == genre_id)

        if author_id := filters.get("author_id"):
            conditions.append(Book.author_id == author_id)

        if min_stars := filters.get("min_stars"):
            conditions.append(Review.stars >= min_stars)

        if max_stars := filters.get("max_stars"):
            conditions.append(Review.stars <= max_stars)

        if conditions:
            query = query.where(and_(*conditions))

        return query

    def _apply_ordering(self, query, order_by: str):
        if order_by == "newest":
            query = query.order_by(desc(Review.created_at))
        elif order_by == "oldest":
            query = query.order_by(asc(Review.created_at))
        elif order_by == "highest_rated":
            query = query.order_by(desc(Review.stars), desc(Review.created_at))

        return query

    async def get_recent_activity(self, days: int = 7, limit: int = 10) -> List[Review]:
        time_threshold = datetime.utcnow() - timedelta(days=days)

        likes_subquery = (
            select(Like.review_id, func.count(Like.review_id).label("likes_count"))
            .group_by(Like.review_id)
            .subquery()
        )

        query = (
            select(
                Review,
                func.coalesce(likes_subquery.c.likes_count, 0).label("likes_count"),
            )
            .join(Review.user)
            .join(Review.book)
            .join(Book.author)
            .join(Book.genre)
            .outerjoin(likes_subquery, likes_subquery.c.review_id == Review.id)
            .where(Review.created_at >= time_threshold)
            .order_by(desc(Review.created_at))
            .limit(limit)
            .options(
                joinedload(Review.user),
                joinedload(Review.book).joinedload(Book.author),
                joinedload(Review.book).joinedload(Book.genre),
            )
        )

        result = await self.session.execute(query)
        rows = result.all()

        reviews = []
        for review, likes_count in rows:
            review.likes_count = likes_count
            reviews.append(review)

        return reviews

    async def get_likes_count_for_review(self, review_id: int) -> int:
        query = select(func.count(Like.id)).where(Like.review_id == review_id)
        result = await self.session.execute(query)
        return result.scalar() or 0
