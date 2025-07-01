import urllib.parse

import pytest
from sqlalchemy import delete

from src.database.db import Session
from src.database.models.users import User


@pytest.fixture
def user(client_sync):
    with Session() as session:
        stmt = delete(User)
        session.execute(stmt)
        session.commit()
    user_data = {
        "username": "username",
        "password": "<PASSWORD>",
    }
    client_sync.post(f"/api/v1/users?{urllib.parse.urlencode(user_data)}")
    yield user_data
