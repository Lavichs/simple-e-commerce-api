import urllib.parse

import pytest
from sqlalchemy import delete

from src.database.db import Session
from src.database.models.products import Product


@pytest.fixture
def products(client_sync):
    with Session() as session:
        stmt = delete(Product)
        session.execute(stmt)
        session.commit()
    products_data = [
        {
            "title": "Product 1",
            "description": "description",
            "price": 100,
            "stock_count": 100,
        },
        {
            "title": "Product 2",
            "description": "description",
            "price": 100,
            "stock_count": 100,
        },
        {
            "title": "Product 3",
            "description": "description",
            "price": 100,
            "stock_count": 100,
        },
    ]
    products = []
    for product in products_data:
        response = client_sync.post(f"/api/v1/products?{urllib.parse.urlencode(product)}")
        products.append(response.json())
    return products
