from src.repositories.products import ProductsRepository
from src.repositories.users import UsersRepository
from src.services.products import ProductsService
from src.services.users import UserService


def products_service() -> ProductsService:
    return ProductsService(ProductsRepository)

def users_service() -> UserService:
    return UserService(UsersRepository)
