from sqladmin import ModelView
from starlette.requests import Request

from models import Review

class ReviewAdmin(ModelView, model=Review):
    column_list = [
        Review.id,
        Review.title,
        Review.stars,
        Review.user_id,
        Review.book_id,
        Review.created_at,
        Review.updated_at,
    ]
    
    def is_accessible(self, request: Request) -> bool:
        return request.session.get("role") in ["admin", "moderator"]
    
    def is_visible(self, request: Request) -> bool:
        return request.session.get("role") in ["admin", "moderator"]