from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Author
from repositories.base_repository import BaseRepository


class AuthorRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Author, session)

    async def get_by_name(self, name: str, surname: str) -> Optional[Author]:
        result = await self.session.execute(
            select(self.model).where(
                self.model.name == name, self.model.surname == surname
            )
        )

        return result.scalar_one_or_none()

    async def search_authors(self, search_term: str, limit: int = 20) -> List[Author]:
        result = await self.session.execute(
            select(self.model)
            .where(
                (self.model.name.ilike(f"%{search_term}%"))
                | (self.model.surname.ilike(f"%{search_term}%"))
                | (self.model.patronymic.ilike(f"%{search_term}%"))
            )
            .limit(limit)
        )
        return result.scalars.all()
