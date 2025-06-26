from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config.config import settings

engine = create_async_engine(settings.DB_URL_ASYNC)
engine_sync = create_engine(settings.DB_URL_SYNC)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
Session = sessionmaker(bind=engine_sync)


class BaseModel(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session
