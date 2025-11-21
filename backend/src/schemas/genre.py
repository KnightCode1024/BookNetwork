from pydantic import BaseModel, ConfigDict


class BaseGenre(BaseModel):
    name: str


class CreateGenre(BaseGenre): ...


class GenreResponse(BaseGenre):
    id: int
    model_config = ConfigDict(from_attributes=True)

class GenreUpdate(BaseGenre):
    pass
