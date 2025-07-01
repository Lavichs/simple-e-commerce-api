import pytest
import pytest_asyncio
from sqlalchemy.exc import ProgrammingError
from httpx import AsyncClient, ASGITransport
from sqlalchemy_utils import create_database, drop_database
from starlette.testclient import TestClient

from app import app
from config.config import settings
from src.database.db import BaseModel, engine_sync


@pytest.fixture(scope="session", autouse=True)
def setup():
    assert settings.MODE == 'TEST'
    print("setup")
    # BaseModel.metadata.drop_all(engine_sync)
    # BaseModel.metadata.create_all(engine_sync)
    try:
        create_database(settings.DB_URL_SYNC)
        BaseModel.metadata.create_all(engine_sync)
        yield settings.DB_URL_ASYNC
    except ProgrammingError:
        yield settings.DB_URL_ASYNC
    finally:
        pass
        drop_database(settings.DB_URL_SYNC)
        return


@pytest.fixture
def clear_db():
    assert settings.MODE == 'TEST'
    try:
        BaseModel.metadata.drop_all(engine_sync)
        BaseModel.metadata.create_all(engine_sync)
    except Exception as e:
        print(e)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def client_async():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.fixture(scope="session", autouse=True)
def client_sync():
    with TestClient(app=app) as client:
        yield client
