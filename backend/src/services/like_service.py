from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from models import Like, Review, User
from repositories import LikeRepository, ReviewRepository


class LikeService:
    def __init__(self, session: AsyncSession):
        self.like_repo = LikeRepository(session)
        self.review_repo = ReviewRepository(session)

    async def like_review(self, user_id: int, review_id: int) -> Optional[Like]:
        review = await self.review_repo.get_by_id(review_id)
        if not review:
            return None

        already_liked = await self.check_user_liked(user_id, review_id)
        if already_liked:
            return None

        return await self.like_repo.create_like(user_id, review_id)

    async def unlike_review(self, user_id: int, review_id: int) -> bool:
        return await self.like_repo.delete_like(user_id, review_id)

    async def get_review_likes_stats(
        self, review_id: int, current_user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        return await self.like_repo.get_like_stats(review_id, current_user_id)

    async def get_user_likes(self, user_id: int) -> list:
        return await self.like_repo.get_likes_by_user(user_id)

    async def check_user_liked(self, user_id: int, review_id: int) -> bool:
        return await self.like_repo.is_liked_by_user(user_id, review_id)
