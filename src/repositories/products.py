from src.database.models.products import Product
from src.schemas.products import SProduct
from src.utils.repository import SQLAlchemyRepository


class ProductsRepository(SQLAlchemyRepository):
    model = Product
    schema = SProduct
