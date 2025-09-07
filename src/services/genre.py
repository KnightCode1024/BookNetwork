from db.repositories.genre import GenreRepository


class GenreService:
    def __init__(self, genre_repository: GenreRepository):
        self.genre_repository = genre_repository

    async def get_all_genres(self):
        return await self.genre_repository.get_all()
