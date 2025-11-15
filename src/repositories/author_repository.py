from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import User
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)
