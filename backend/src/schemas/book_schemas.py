from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, validator


class BookBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Название книги",
    )
    description: str = Field(
        ...,
        min_length=1,
        description="Описание книги",
    )
    publication_year: int = Field(
        ...,
        ge=1000,
        le=datetime.now().year,
        description="Год публикации",
    )
    author_id: int = Field(
        ...,
        ge=1,
        description="ID автора",
    )
    genre_id: int = Field(
        ...,
        ge=1,
        description="ID жанра",
    )

    @validator("title")
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Название книги не может быть пустым")
        return v.strip()

    @validator("description")
    def description_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Описание книги не может быть пустым")
        return v.strip()


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Название книги",
    )
    description: Optional[str] = Field(
        None,
        min_length=1,
        description="Описание книги",
    )
    publication_year: Optional[int] = Field(
        None,
        ge=1000,
        le=datetime.now().year,
        description="Год публикации",
    )
    author_id: Optional[int] = Field(
        None,
        ge=1,
        description="ID автора",
    )
    genre_id: Optional[int] = Field(
        None,
        ge=1,
        description="ID жанра",
    )

    @validator("title")
    def title_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Название книги не может быть пустым")
        return v.strip() if v else v

    @validator("description")
    def description_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Описание книги не может быть пустым")
        return v.strip() if v else v


class BookResponse(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author: Optional["AuthorSearchResponse"] = None
    genre: Optional["GenreResponse"] = None

    model_config = ConfigDict(from_attributes=True)


class BookShortResponse(BaseModel):
    id: int
    title: str
    publication_year: int
    author_id: int
    genre_id: int

    model_config = ConfigDict(from_attributes=True)


from schemas.author_schemas import AuthorSearchResponse
from schemas.genre_schemas import GenreResponse

BookResponse.model_rebuild()
