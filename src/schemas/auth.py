from typing import Annotated
from annotated_types import MaxLen, MinLen

from pydantic import BaseModel, EmailStr, ConfigDict, Field

class CreateUser(BaseModel):
    username: Annotated[str, MinLen(2), MaxLen(30)]
    email: EmailStr | None = None

class UserSchema(CreateUser):
    model_config = ConfigDict(strict=True)
    password: str = Field(..., min_length=6)
    is_active: bool = True

class LoginSchema(BaseModel):
    username: str
    password: str

class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshTokenSchema(BaseModel):
    refresh_token: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"