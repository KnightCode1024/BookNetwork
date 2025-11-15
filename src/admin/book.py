from sqladmin import ModelView
from starlette.requests import Request

from models import Book


class BookAdmin(ModelView, model=Book):
    column_list = [
        Book.id,
        Book.title,
        Book.publication_year,
        Book.author_id,
        Book.genre_id,
        Book.created_at,
        Book.updated_at,
    ]

    def is_accessible(self, request: Request) -> bool:
        return request.session.get("role") in ["admin", "moderator"]

    def is_visible(self, request: Request) -> bool:
        return request.session.get("role") in ["admin", "moderator"]
