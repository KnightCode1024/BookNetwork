from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import IntEnum
from datetime import datetime

from models.review import ReviewStars

class ReviewBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Заголовок отзыва")
    content: str = Field(..., min_length=1, max_length=2000, description="Содержание отзыва")
    stars: ReviewStars = Field(..., description="Рейтинг от 1 до 5 звезд")
    book_id: int = Field(..., gt=0, description="ID книги")

    @validator('content')
    def content_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Содержание отзыва не может быть пустым')
        return v.strip()


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Заголовок отзыва")
    content: Optional[str] = Field(None, min_length=1, max_length=2000, description="Содержание отзыва")
    stars: Optional[ReviewStars] = Field(None, description="Рейтинг от 1 до 5 звезд")

    @validator('content')
    def content_not_empty_if_present(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Содержание отзыва не может быть пустым')
            return v.strip()
        return v


class UserSimpleResponse(BaseModel):
    id: int
    username: str
    
    class Config:
        from_attributes = True


class AuthorSimpleResponse(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: str
    
    @property
    def display_name(self):
        return f"{self.name[0].upper()}.{self.patronymic[0].upper()}.{self.surname.capitalize()}"
    
    class Config:
        from_attributes = True


class GenreSimpleResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True


class BookSimpleResponse(BaseModel):
    id: int
    title: str
    publication_year: int
    author: AuthorSimpleResponse
    genre: GenreSimpleResponse
    
    class Config:
        from_attributes = True


class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: Optional[UserSimpleResponse] = None
    book: Optional[BookSimpleResponse] = None
    
    class Config:
        from_attributes = True


class ReviewDetailResponse(ReviewResponse):
    user: UserSimpleResponse
    book: BookSimpleResponse
    
    class Config:
        from_attributes = True

class ReviewListResponse(BaseModel):
    items: List[ReviewResponse]
    total: int
    offset: int
    limit: int
    has_more: bool
    
    class Config:
        from_attributes = True


class ReviewStatsResponse(BaseModel):
    total_reviews: int
    average_rating: float
    rating_distribution: dict
    user_review_count: Optional[int] = None
    
    class Config:
        from_attributes = True
