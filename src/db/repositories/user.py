from sqlalchemy.ext.asyncio import AsyncSession

from db.models.user import User
from db.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_user_by_tg_id(self, tg_id):
        return await self.get(tg_id=tg_id)
