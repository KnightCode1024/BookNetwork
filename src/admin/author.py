from sqladmin import ModelView
from starlette.requests import Request

from models import Author

class AuthorAdmin(ModelView, model=Author):
    column_list = [
        Author.id,
        Author.name,
        Author.surname,
        Author.patronymic,
        Author.date_birth,
        Author.date_death,
        Author.created_at,
        Author.updated_at,
    ]
    
    def is_accessible(self, request: Request) -> bool:
        return request.session.get("role") in ["admin", "moderator"]
    
    def is_visible(self, request: Request) -> bool:
        return request.session.get("role") in ["admin", "moderator"]