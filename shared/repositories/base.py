from typing import Generic, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, object_id: int) -> ModelType | None:
        return await self.db.get(self.model, object_id)

    async def get_all(self, limit: int, offset: int) -> list[ModelType]:
        query = select(self.model).order_by(self.model.id).offset(offset).limit(limit)
        result = await self.db.scalars(query)
        objects = result.all()
        return objects

    async def create(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        return obj

    async def update(self, obj: ModelType) -> ModelType:
        return obj

    async def delete(self, obj: ModelType) -> None:
        await self.db.delete(obj)
        return None