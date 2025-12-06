from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from models import Review, User
from repositories import ReviewRepository


class ReviewService:
    def __init__(self, session: AsyncSession):
        self.review_repo = ReviewRepository(session)

    async def get_review_by_id(self, review_id: int) -> Optional[Review]:
        return await self.review_repo.get_review_by_id_with_details(review_id)

    async def get_reviews_by_book_id(
        self, 
        book_id: int, 
        offset: int = 0, 
        limit: int = 20
    ) -> List[Review]:
        return await self.review_repo.get_reviews_by_book_id(book_id, offset, limit)

    async def get_reviews_by_user_id(
        self, 
        user_id: int, 
        offset: int = 0, 
        limit: int = 20
    ) -> List[Review]:
        return await self.review_repo.get_reviews_by_user_id(user_id, offset, limit)

    async def create_review(self, user_id: int, review_data: dict) -> Review:
        return await self.review_repo.create_review(user_id, review_data)

    async def update_review(
        self, 
        review_id: int, 
        user: User, 
        review_data: dict
    ) -> Optional[Review]:
        can_modify = await self.review_repo.can_user_modify_review(review_id, user.id)
        if not can_modify and user.role.value != "admin":
            return None
        
        return await self.review_repo.update_review(review_id, review_data)

    async def delete_review(self, review_id: int, user: User) -> bool:
        can_delete = await self.review_repo.can_user_modify_review(review_id, user.id)
        if not can_delete and user.role.value != "admin":
            return False
        
        return await self.review_repo.delete(review_id)

    async def get_review_stats_by_book_id(self, book_id: int) -> Dict[str, Any]:
        return await self.review_repo.get_review_stats_by_book_id(book_id)

    async def user_has_review_for_book(self, user_id: int, book_id: int) -> bool:
        review = await self.review_repo.get_user_review_for_book(user_id, book_id)
        return review is not None

    async def get_user_review_for_book(self, user_id: int, book_id: int) -> Optional[Review]:
        return await self.review_repo.get_user_review_for_book(user_id, book_id)
