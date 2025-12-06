from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, desc, asc
from sqlalchemy.orm import selectinload, joinedload

from models import Review, Book, Author, Genre, User


class FeedRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_feed(
        self,
        offset: int = 0,
        limit: int = 20,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Review]:
        query = (
            select(Review)
            .join(Review.user)
            .join(Review.book)
            .join(Book.author)
            .join(Book.genre)
            .options(
                joinedload(Review.user),
                joinedload(Review.book)
                .joinedload(Book.author),
                joinedload(Review.book)
                .joinedload(Book.genre),
            )
        )

        if filters:
            query = self._apply_filters(query, filters)

        query = self._apply_ordering(query, filters.get('order_by') if filters else 'newest')

        query = query.offset(offset).limit(limit)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_feed_with_stats(
        self,
        offset: int = 0,
        limit: int = 20,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        reviews = await self.get_feed(offset, limit, filters)
        
        count_query = select(func.count(Review.id))
        if filters:
            count_query = self._apply_filters(count_query, filters)
        
        result = await self.session.execute(count_query)
        total = result.scalar()
        
        return {
            "reviews": reviews,
            "total": total,
            "offset": offset,
            "limit": limit,
            "has_more": (offset + limit) < total
        }

    def _apply_filters(self, query, filters: Dict[str, Any]):        
        conditions = []
        
        if book_id := filters.get('book_id'):
            conditions.append(Review.book_id == book_id)
        
        if user_id := filters.get('user_id'):
            conditions.append(Review.user_id == user_id)
        
        if genre_id := filters.get('genre_id'):
            conditions.append(Book.genre_id == genre_id)
        
        if author_id := filters.get('author_id'):
            conditions.append(Book.author_id == author_id)
        
        if min_stars := filters.get('min_stars'):
            conditions.append(Review.stars >= min_stars)
        
        if max_stars := filters.get('max_stars'):
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

    async def get_recent_activity(
        self,
        days: int = 7,
        limit: int = 10
    ) -> List[Review]:
        time_threshold = datetime.utcnow() - timedelta(days=days)
        
        query = (
            select(Review)
            .join(Review.user)
            .join(Review.book)
            .join(Book.author)
            .join(Book.genre)
            .where(Review.created_at >= time_threshold)
            .order_by(desc(Review.created_at))
            .limit(limit)
            .options(
                selectinload(Review.user),
                selectinload(Review.book)
                .selectinload(Book.author),
                selectinload(Review.book)
                .selectinload(Book.genre),
            )
        )
        
        result = await self.session.execute(query)
        return result.scalars().all()
