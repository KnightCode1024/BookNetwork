from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from models.review import ReviewStars


class AuthorFeedResponse(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: str

    @property
    def display_name(self):
        return f"{self.name[0].upper()}.{self.patronymic[0].upper()}.{self.surname.capitalize()}"

    class Config:
        from_attributes = True


class GenreFeedResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class BookFeedResponse(BaseModel):
    id: int
    title: str
    description: str
    publication_year: int
    author: AuthorFeedResponse
    genre: GenreFeedResponse

    class Config:
        from_attributes = True


class UserFeedResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class ReviewFeedResponse(BaseModel):
    id: int
    title: str
    content: str
    stars: ReviewStars
    likes_count: int
    created_at: datetime
    updated_at: datetime

    user: UserFeedResponse
    book: BookFeedResponse

    class Config:
        from_attributes = True


class FeedResponse(BaseModel):
    reviews: List[ReviewFeedResponse]
    total: int
    offset: int
    limit: int
    has_more: bool

    class Config:
        from_attributes = True


class FeedFilters(BaseModel):
    book_id: Optional[int] = None
    user_id: Optional[int] = None
    genre_id: Optional[int] = None
    author_id: Optional[int] = None
    min_stars: Optional[int] = Field(None, ge=1, le=5)
    max_stars: Optional[int] = Field(None, ge=1, le=5)
    order_by: Optional[str] = Field("newest", pattern="^(newest|oldest|highest_rated)$")
