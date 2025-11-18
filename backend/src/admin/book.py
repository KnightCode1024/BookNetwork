from sqladmin import ModelView
from starlette.requests import Request

from models import Book


class BookAdmin(ModelView, model=Book):
    column_list = [
        Book.id,
        Book.title,
        Book.publication_year,
        Book.author,
        Book.genre,
        Book.created_at,
        Book.updated_at,
    ]

    column_details_list = [
        Book.id,
        Book.title,
        Book.description,
        Book.publication_year,
        Book.author,
        Book.genre,
        Book.created_at,
        Book.updated_at,
    ]

    form_columns = [
        Book.title,
        Book.description,
        Book.publication_year,
        Book.author,
        Book.genre,
    ]

    form_ajax_refs = {
        "author": {
            "fields": ("name", "surname"),
            "order_by": ("surname", "name"),
        },
        "genre": {
            "fields": ("name",),
            "order_by": ("name",),
        },
    }

    def is_accessible(self, request: Request) -> bool:
        return request.session.get("role") in ["admin", "moderator"]

    def is_visible(self, request: Request) -> bool:
        return request.session.get("role") in ["admin", "moderator"]
