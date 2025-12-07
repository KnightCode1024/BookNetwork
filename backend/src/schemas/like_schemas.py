from datetime import datetime

from pydantic import BaseModel


class LikeBase(BaseModel):
    review_id: int


class LikeCreate(LikeBase):
    pass


class LikeResponse(LikeBase):
    user_id: int
    created_at: datetime

    class Config:
        from_atributes = True


class LikeStatsResponse(LikeBase):
    like_count: int
    user_liked: bool = False

    class Config:
        from_atributes = True
