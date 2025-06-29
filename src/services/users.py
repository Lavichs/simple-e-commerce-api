import uuid

import bcrypt

from src.schemas.users import SUser, SUserAdd
from src.utils.repository import AbstractRepository


class UsersService:
    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    async def sign_in(self, user: SUserAdd, is_admin: bool = False) -> uuid.UUID:
        password = bytes(user.password, "utf-8")
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        user_to_db = SUser(
            id=uuid.uuid4(),
            username=user.username,
            hashed_password=hashed,
            is_admin=is_admin
        )
        user = await self.repository.add(user_to_db.model_dump())
        return user.id


