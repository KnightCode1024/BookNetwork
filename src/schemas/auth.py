from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr, ConfigDict

class CreateUser(BaseModel):
    username: Annotated[str, MinLen(2), MaxLen(30)]
    email: EmailStr | None = None


class UserSchema(CreateUser):
    model_config = ConfigDict(strict=True)

    password: bytes
    is_active: bool = True


class TokenInfo(BaseModel):
    access_token: str
    token_type: str

class LoginSchema(BaseModel):
    username: str
    password: str
