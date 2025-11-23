from sqladmin import ModelView
from starlette.requests import Request

from models import Genre


class GenreAdmin(ModelView, model=Genre):
    column_list = [
        Genre.id,
        Genre.name,
    ]

    form_columns = [Genre.name]

    def is_accessible(self, request: Request) -> bool:
        return request.session.get("role") in ["admin", "moderator"]

    def is_visible(self, request: Request) -> bool:
        return request.session.get("role") in ["admin", "moderator"]
