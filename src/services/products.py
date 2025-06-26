import uuid

from src.schemas.products import SProductAdd, SProduct
from src.utils.repository import AbstractRepository


class ProductsService:
    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    async def add(self, product: SProductAdd):
        product_dict = product.model_dump()
        product_to_db = SProduct(**product_dict, id=uuid.uuid4())
        product_dict = product_to_db.model_dump()
        product = await self.repository.add(product_dict)
        return product

    async def get_all(self):
        products = await self.repository.get_all()
        return products

