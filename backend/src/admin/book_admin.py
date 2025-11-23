from sqladmin import ModelView
from starlette.requests import Request

from models import Book, Author, Genre


class BookAdmin(ModelView, model=Book):
    column_list = [
        Book.id,
        Book.title,
        Book.author,  # Показывает связанного автора
        Book.genre,   # Показывает связанный жанр
        Book.publication_year,
    ]

    column_labels = {
        Book.author: "Автор",
        Book.genre: "Жанр"
    }

    form_columns = [
        Book.title,
        Book.description,
        Book.publication_year,
        Book.author,  # Теперь используем связь, а не ID
        Book.genre,   # Теперь используем связь, а не ID
    ]

    def is_accessible(self, request: Request) -> bool:
        return request.session.get("role") in ["admin", "moderator"]

    def is_visible(self, request: Request) -> bool:
        return request.session.get("role") in ["admin", "moderator"]
