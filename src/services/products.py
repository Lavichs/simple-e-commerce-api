import uuid

from src.schemas.products import SProductAdd, SProduct
from src.utils.repository import AbstractRepository


class ProductsService:
    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    async def add(self, product: SProductAdd) -> SProduct:
        product_dict = product.model_dump()
        product_to_db = SProduct(**product_dict, id=uuid.uuid4())
        product_dict = product_to_db.model_dump()
        product = await self.repository.add(product_dict)
        return product

    async def get_all(self) -> list[SProduct]:
        products = await self.repository.get_all()
        return products

    async def get_by_id(self, id: uuid.UUID) -> SProduct | None:
        product = await self.repository.get_by_id(id)
        return product

    async def update(self, id: uuid.UUID, product: SProductAdd) -> SProduct | bool:
        product_dict = product.model_dump()
        is_product_update = await self.repository.update(id, product_dict)
        if is_product_update:
            return await self.repository.get_by_id(id)
        else:
            return is_product_update

    async def delete(self, id: uuid.UUID):
        await self.repository.delete(id)


