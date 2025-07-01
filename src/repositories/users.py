from sqlalchemy import select

from src.database.db import async_session_maker
from src.database.models.users import User
from src.schemas.users import SUser
from src.utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User
    schema = SUser

    async def get_by_username(self, username: str):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.username == username)
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model is None:
                return None
            return self.schema.model_validate(model)
