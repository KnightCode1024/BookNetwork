from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from models import Review, Book, User
from repositories import BaseRepository


class ReviewRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Review, session)

    async def get_review_by_id_with_details(self, review_id: int) -> Optional[Review]:
        query = (
            select(self.model)
            .where(self.model.id == review_id)
            .options(
                selectinload(self.model.user),
                selectinload(self.model.book)
                .selectinload(Book.author),
                selectinload(self.model.book)
                .selectinload(Book.genre),
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_reviews_by_book_id(
        self, 
        book_id: int, 
        offset: int = 0, 
        limit: int = 20
    ) -> List[Review]:
        query = (
            select(self.model)
            .where(self.model.book_id == book_id)
            .offset(offset)
            .limit(limit)
            .options(
                selectinload(self.model.user),
            )
            .order_by(self.model.created_at.desc())
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_reviews_by_user_id(
        self, 
        user_id: int, 
        offset: int = 0, 
        limit: int = 20
    ) -> List[Review]:
        query = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .offset(offset)
            .limit(limit)
            .options(
                selectinload(self.model.book)
                .selectinload(Book.author),
                selectinload(self.model.book)
                .selectinload(Book.genre),
            )
            .order_by(self.model.created_at.desc())
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_review(self, user_id: int, data: dict) -> Review:
        existing_review = await self.get_user_review_for_book(user_id, data.get('book_id'))
        if existing_review:
            raise ValueError("Вы уже оставили отзыв для этой книги")

        data_with_user = {**data, 'user_id': user_id}
        return await self.create(data_with_user)

    async def update_review(self, review_id: int, data: dict) -> Optional[Review]:
        instance = await self.get_by_id(review_id)
        if not instance:
            return None
        
        for key, value in data.items():
            if value is not None and hasattr(instance, key):
                setattr(instance, key, value)
        
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def can_user_modify_review(self, review_id: int, user_id: int) -> bool:
        query = select(self.model).where(
            self.model.id == review_id,
            self.model.user_id == user_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def get_user_review_for_book(self, user_id: int, book_id: int) -> Optional[Review]:
        query = select(self.model).where(
            self.model.user_id == user_id,
            self.model.book_id == book_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_review_stats_by_book_id(self, book_id: int) -> dict:
        from sqlalchemy import func
        
        query = select(
            func.count(self.model.id).label('total_reviews'),
            func.avg(self.model.stars).label('average_rating'),
            func.min(self.model.stars).label('min_rating'),
            func.max(self.model.stars).label('max_rating')
        ).where(self.model.book_id == book_id)
        
        result = await self.session.execute(query)
        stats = result.first()
        
        return {
            'total_reviews': stats.total_reviews or 0,
            'average_rating': float(stats.average_rating or 0),
            'min_rating': stats.min_rating or 0,
            'max_rating': stats.max_rating or 0
        }
