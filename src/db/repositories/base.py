from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update


class BaseRepository:
    def __init__(self, session: AsyncSession, model):
        self.session = session
        self.model = model

    async def add(self, entity):
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def get(self, id):
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_pk(self, **pk_filters):
        if not pk_filters:
            raise ValueError("PK not found")

        query = select(self.model)
        for key, value in pk_filters.items():
            if not hasattr(self.model, key):
                raise ValueError(
                    f"Field {key} not exists in model {self.model.__name__}"
                )
            query = query.where(getattr(self.model, key) == value)

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100):
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update(self, id, **kwargs):
        entity = await self.get(id)
        if not entity:
            return None

        for key, value in kwargs.items():
            if hasattr(entity, key):
                setattr(entity, key, value)

        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update_by_filter(self, filters: dict, **update_data):
        if not update_data:
            return None

        query = update(self.model)
        for key, value in filters.items():
            query = query.where(getattr(self.model, key) == value)

        query = query.values(**update_data)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount

    async def delete(self, id):
        entity = await self.get(id)
        if not entity:
            return None

        await self.session.delete(entity)
        await self.session.commit()
