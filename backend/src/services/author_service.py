from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from models import Author
from repositories import AuthorRepository


class AuthorService:
    def __init__(self, session: AsyncSession):
        self.author_repo = AuthorRepository(session)

    async def get_author_by_id(self, author_id: int) -> Optional[Author]:
        return await self.author_repo.get_by_id(author_id)

    async def get_all_authors(self, offset: int = 0, limit: int = 20) -> List[Author]:
        return await self.author_repo.get_all(offset, limit)

    async def create_author(self, author_data: dict) -> Author:
        self._validate_dates(author_data)
        return await self.author_repo.create(author_data)

    async def update_author(self, author_id: int, author_data: dict) -> Optional[Author]:
        self._validate_dates(author_data)
        return await self.author_repo.update(author_id, author_data)

    async def partial_update_author(self, author_id: int, author_data: dict) -> Optional[Author]:
        update_data = {k: v for k, v in author_data.items() if v is not None}
        self._validate_dates(update_data)
        return await self.author_repo.update(author_id, update_data)

    async def delete_author(self, author_id: int) -> bool:
        return await self.author_repo.delete(author_id)

    async def get_author_by_name(self, name: str, surname: str) -> Optional[Author]:
        return await self.author_repo.get_by_name(name, surname)

    async def search_authors(self, search_term: str, limit: int = 20) -> List[Author]:
        return await self.author_repo.search_authors(search_term, limit)

    def _validate_dates(self, author_data: dict):
        if 'date_birth' in author_data and author_data['date_birth']:
            if isinstance(author_data['date_birth'], str):
                try:
                    author_data['date_birth'] = datetime.fromisoformat(author_data['date_birth'].replace('Z', '+00:00'))
                except ValueError:
                    raise ValueError("Invalid date_birth format")
        
        if 'date_death' in author_data and author_data['date_death']:
            if isinstance(author_data['date_death'], str):
                try:
                    author_data['date_death'] = datetime.fromisoformat(author_data['date_death'].replace('Z', '+00:00'))
                except ValueError:
                    raise ValueError("Invalid date_death format")

        date_birth = author_data.get('date_birth')
        date_death = author_data.get('date_death')
        
        if date_birth and date_death and date_death < date_birth:
            raise ValueError("Date of death cannot be earlier than date of birth")