from sqladmin import ModelView
from starlette.requests import Request

from models import User


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.email,
        User.role,
        User.is_active,
        # User.created_at,
        # User.updated_at,
    ]

    form_columns = [
        User.created_at,
        User.updated_at,
    ]

    def is_accessible(self, request: Request) -> bool:
        return request.session.get("role") == "admin"

    def is_visible(self, request: Request) -> bool:
        return request.session.get("role") == "admin"
