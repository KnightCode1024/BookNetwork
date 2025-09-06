from pydantic import BaseModel


class UserCreate(BaseModel):
    tg_id: int
    username: str | None
    first_name: str
    last_name: str | None
