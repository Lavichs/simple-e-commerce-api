from src.repositories.products import ProductsRepository
from src.services.products import ProductsService


def products_service():
    return ProductsService(ProductsRepository)
