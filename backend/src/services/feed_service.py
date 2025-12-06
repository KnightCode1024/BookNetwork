from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import FeedRepository
from schemas.feed_schemas import FeedResponse, ReviewFeedResponse


class FeedService:
    def __init__(self, session: AsyncSession):
        self.feed_repo = FeedRepository(session)

    async def get_feed(
        self,
        offset: int = 0,
        limit: int = 20,
        filters: Optional[Dict[str, Any]] = None
    ) -> FeedResponse:
        
        feed_data = await self.feed_repo.get_feed_with_stats(offset, limit, filters)

        review_responses = [
            ReviewFeedResponse.from_orm(review)
            for review in feed_data["reviews"]
        ]
        
        return FeedResponse(
            reviews=review_responses,
            total=feed_data["total"],
            offset=feed_data["offset"],
            limit=feed_data["limit"],
            has_more=feed_data["has_more"]
        )

    async def get_recent_activity(
        self,
        days: int = 7,
        limit: int = 10
    ) -> List[ReviewFeedResponse]:
        
        reviews = await self.feed_repo.get_recent_activity(days, limit)
        
        return [
            ReviewFeedResponse.from_orm(review)
            for review in reviews
        ]
