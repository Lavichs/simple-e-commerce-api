import urllib.parse
import uuid

import pytest
from contextlib import nullcontext as does_not_raise
from src.schemas.products import SProduct

invalid_test_product_data = [
    ("title", "description", 0, 0, 422),
    ("title", "description", 100.5, 100.74, 422),
    ("title", "description", -100, 100, 422),
    ("title", "description", 100, -100, 422),
    ("", "", 100, 100, 422),
    ("", "a" * 2000, 100, 100, 422),
    (None, None, None, None, 422),
    ("title", "description", "eee", 100, 422),
    ("title", "description", 100, None, 422),
]


class TestProducts:
    @pytest.mark.parametrize(
        "title, description, price, stock_count, status",
        [
                ("title", "description", 100, 100, 201),
                ("title", "description", 100.5, 100, 201),
                ("title", "description", 100, 0, 201),
        ] + invalid_test_product_data
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
        assert response.json() == products

    def test_get_by_id(self, client_sync, product):
        response = client_sync.get(f"/api/v1/products/{product.get('id')}?")
        assert response.status_code == 200
        assert SProduct(**response.json())
        response = client_sync.get(f"/api/v1/products/{uuid.uuid4()}?")
        assert response.status_code == 404
        assert response.json() == {'detail': 'Product not found'}

    @pytest.mark.parametrize(
        "title, description, price, stock_count, status",
        [
            ("title", "description", 100, 100, 200),
            ("title", "description", 100.5, 100, 200),
            ("title", "description", 100, 0, 200),
        ] + invalid_test_product_data
    )
    def test_update_product(self, client_sync, product, title, description, price, stock_count, status):
        product_data = {
            "title": title,
            "description": description,
            "price": price,
            "stock_count": stock_count,
        }
        response = client_sync.put(f"/api/v1/products/{product.get('id')}?{urllib.parse.urlencode(product_data)}")
        assert response.status_code == status

    def test_update_product_negative(self, client_sync):
        product_data = {
            "title": "title",
            "description": "description",
            "price": 100,
            "stock_count": 100,
        }
        response = client_sync.put(f"/api/v1/products/{uuid.uuid4()}?{urllib.parse.urlencode(product_data)}")
        assert response.status_code == 404

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
