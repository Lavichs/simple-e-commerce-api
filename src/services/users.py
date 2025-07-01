import uuid
from datetime import datetime, timedelta

import bcrypt
from fastapi import HTTPException, status

from config.config import settings
from config.jwt_auth import security
from src.repositories.users import UsersRepository
from src.schemas.users import SUser, SUserAdd
from src.utils.repository import AbstractRepository


class UserService:
    def __init__(self, repository: UsersRepository):
        self.repository: UsersRepository = repository()

    async def sign_in(self, user: SUserAdd, is_admin: bool = False) -> uuid.UUID:
        candidate: SUser | None = await self.repository.get_by_username(user.username)
        if candidate is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The user's name is occupied")
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

    async def login(self, user: SUserAdd):
        candidate: SUser | None = await self.repository.get_by_username(user.username)
        print(candidate)
        if candidate is None:
            return False
        if bcrypt.checkpw(bytes(user.password, 'utf-8'), candidate.hashed_password):
            expire = datetime.now() + timedelta(minutes=settings.JWT_EXPIRATION_DELTA)
            token = security.create_access_token(uid=str(candidate.id), expires_delta=expire)
            return token
        else:
            return False


