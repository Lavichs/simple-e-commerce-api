import urllib.parse

import pytest

from src.schemas.users import SUserAdd


class TestUsers:
    @pytest.mark.parametrize(
        "username, password, status",
        [
            ("username", "<PASSWORD>", 201),
            ("username", "<PASSWORD>", 409),  # duplicate usernames
            ("usr", "<PASSWORD>", 201),
            ("usr", "psw", 422),
            ("usr", "", 422),
            ("", "<PASSWORD>", 422),
            ("", "", 422),
        ]
    )
    def test_sign_in(self, client_sync, username, password, status):
        user_data = {
            "username": username,
            "password": password,
        }
        response = client_sync.post(f"/api/v1/users?{urllib.parse.urlencode(user_data)}")
        assert response.status_code == status

    @pytest.mark.parametrize(
        "username, password, status",
        [
            ("username", "<PASSWORD>", 200),
            ("username", "<_PASSWORD>", 401),
            ("", "<PASSWORD>", 422),
            ("username", "", 422),
            ("", "", 422),
            ("usr", "<PASSWORD>", 401),
        ]
    )
    def test_login(self, client_sync, user, username, password, status):
        user_data = {
            "username": username,
            "password": password,
        }
        response = client_sync.get(f"/api/v1/users/login?{urllib.parse.urlencode(user_data)}")
        assert response.status_code == status

