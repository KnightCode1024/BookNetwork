from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    surname: str
    patronymic: str
    bio: str
    date_birth: datetime = None
    date_death: datetime = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    bio: Optional[str] = None
    date_birth: Optional[datetime] = None
    date_death: Optional[datetime] = None


class AuthorResponse(AuthorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AuthorSearchResponse(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: str

    model_config = ConfigDict(from_attributes=True)
