from typing import Annotated

from fastapi import APIRouter, Depends

from src.api_v1.dependencies import users_service
from src.schemas.users import SUserAdd
from src.services.users import UsersService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/", status_code=201)
async def sign_in(
        user: Annotated[SUserAdd, Depends()],
        user_service: Annotated[UsersService, Depends(users_service)]
):
    user_id = await user_service.sign_in(user)
    return {"id": user_id}

