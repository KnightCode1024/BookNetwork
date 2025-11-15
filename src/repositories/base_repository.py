from typing import Optional, List
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from models import Base


class IRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Base]: ...

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 20) -> List[Base]: ...

    @abstractmethod
    async def create(self, data: dict) -> Base: ...

    @abstractmethod
    async def update(self, id: int, data: dict) -> Optional[Base]: ...

    @abstractmethod
    async def delete(self, id: int) -> bool: ...


class BaseRepository(IRepository):
    def __init__(self, model: Base, session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id: int):
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, offset: int = 0, limit: int = 20):
        result = await self.session.execute(
            select(self.model).offset(offset).limit(limit)
        )
        return result.scalars().all()

    async def create(self, data: dict):
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, id: int, data: dict):
        updated_data = {k: v for k, v in data.items() if v is not None}

        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**updated_data)
            .execution_options(synchronize_session="fetch")
        )

        await self.session.execute(stmt)
        await self.session.commit()

        return await self.get_by_id(id)

    async def delete(self, id: int):
        instance = await self.get_by_id(id)
        if instance:
            await self.session.delete(instance)
            await self.session.commit()
            return True
        return False
