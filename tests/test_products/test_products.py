import urllib.parse
import pytest
from contextlib import nullcontext as does_not_raise
from src.schemas.products import SProduct


class TestProducts:
    @pytest.mark.parametrize(
        "title, description, price, stock_count, status",
        (
                ("title", "description", 100, 100, 201),
                ("title", "description", 100.5, 100, 201),
                ("title", "description", 100, 0, 201),
                ("title", "description", 0, 0, 422),
                ("title", "description", 100.5, 100.74, 422),
                ("title", "description", -100, 100, 422),
                ("title", "description", 100, -100, 422),
                ("", "", 100, 100, 422),
                ("", "a" * 2000, 100, 100, 422),
                (None, None, None, None, 422),
                ("title", "description", "eee", 100, 422),
                ("title", "description", 100, None, 422),
        )
    )
    def test_add_products(self, client_sync, title, description, price, stock_count, status):
        product_data = {
            "title": title,
            "description": description,
            "price": price,
            "stock_count": stock_count,
        }
        response = client_sync.post(f"/api/v1/products?{urllib.parse.urlencode(product_data)}")
        assert response.status_code == status
        if status == 201:
            assert SProduct(**response.json())

    def test_get_all_products(self, client_sync, products):
        response = client_sync.get(f"/api/v1/products?")
        assert response.status_code == 200
        assert response.json().get('data') == products


# class TestPP:
#     @pytest.mark.parametrize(
#         "a, b, c, expectation",
#         [
#             (1, 2, 3, does_not_raise()),
#             (3, 4, 7, does_not_raise()),
#             (5, 6, 11, does_not_raise()),
#             (7, 8, 15, does_not_raise()),
#             (1, "1", 2, pytest.raises(TypeError))
#         ]
#     )
#     def test_add(self, a, b, c, expectation):
#         with expectation:
#             assert a + b == c