from src.database.models.users import User
from src.schemas.users import SUser
from src.utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User
    schema = SUser
