from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from repositories import BaseRepository
from models import Like, Review, User


class LikeRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Like, session)

    async def create_like(self, user_id: int, review_id: int) -> Optional[Like]:
        try:
            like = Like(user_id=user_id, review_id=review_id)
            self.session.add(like)
            await self.session.commit()
            await self.session.refresh(like)
            return like
        except IntegrityError:
            await self.session.rollback()
            return None

    async def delete_like(self, user_id: int, review_id: int) -> bool:
        stmt = delete(Like).where(Like.user_id == user_id, Like.review_id == review_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def get_like(self, user_id: int, review_id: int) -> Optional[Like]:
        stmt = select(Like).where(Like.user_id == user_id, Like.review_id == review_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_likes_by_review(self, review_id: int) -> List[Like]:
        stmt = select(Like).where(Like.review_id == review_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_likes_by_user(self, user_id: int) -> List[Like]:
        stmt = select(Like).where(Like.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_likes_count(self, review_id: int) -> int:
        stmt = select(func.count()).select_from(Like).where(Like.review_id == review_id)
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def is_liked_by_user(self, user_id: int, review_id: int) -> bool:
        like = await self.get_like(user_id, review_id)
        return like is not None

    async def get_like_stats(
        self, review_id: int, current_user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        likes_count = await self.get_likes_count(review_id)

        stats = {
            "review_id": review_id,
            "likes_count": likes_count,
            "user_liked": False,
        }

        if current_user_id:
            stats["user_liked"] = await self.is_liked_by_user(
                current_user_id, review_id
            )

        return stats
