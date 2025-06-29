from src.repositories.products import ProductsRepository
from src.repositories.users import UsersRepository
from src.services.products import ProductsService
from src.services.users import UsersService


def products_service() -> ProductsService:
    return ProductsService(ProductsRepository)

def users_service() -> UsersService:
    return UsersService(UsersRepository)
