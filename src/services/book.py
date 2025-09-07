from db.repositories.book import BookRepository


class BookService:
    def __init__(self, user_repository: BookRepository):
        self.user_repository = user_repository
