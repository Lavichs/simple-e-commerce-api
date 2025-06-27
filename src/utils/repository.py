import uuid
from abc import ABC, abstractmethod
from sqlalchemy import select, insert, update, delete

from src.database.db import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: uuid.UUID):
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: uuid.UUID, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: uuid.UUID):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None
    schema = None

    async def add(self, data: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def get_all(self):
        async with async_session_maker() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            res = [self.schema.model_validate(row[0]) for row in res.all()]
            return res

    async def get_by_id(self, id: uuid.UUID):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == id)
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model is None:
                return None
            return self.schema.model_validate(model)

    async def update(self, id: uuid.UUID, data: dict):
        async with async_session_maker() as session:
            stmt = update(self.model).where(self.model.id == id).values(**data)
            result = await session.execute(stmt)
            await session.commit()
            print(result)
            # print(result.scalar_one_or_none())
            return result.rowcount > 0

    async def delete(self, id: uuid.UUID):
        async with async_session_maker() as session:
            stmt = delete(self.model).where(self.model.id == id)
            result = await session.execute(stmt)
            await session.commit()
            print(result)
            return result.rowcount > 0
