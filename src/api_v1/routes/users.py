from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response

from src.api_v1.dependencies import users_service
from src.schemas.users import SUserAdd
from src.services.users import UserService
from config.jwt_auth import security, config

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/", status_code=201)
async def sign_in(
        user: Annotated[SUserAdd, Depends()],
        user_service: Annotated[UserService, Depends(users_service)]
):
    user_id = await user_service.sign_in(user)
    return {"id": user_id}

@router.get("/login")
async def login(
        response: Response,
        credentials: Annotated[SUserAdd, Depends()],
        user_service: UserService = Depends(users_service),
):
    token = await user_service.login(credentials)
    if token:
        security.set_access_cookies(response=response, token=token)
        return {config.JWT_ACCESS_COOKIE_NAME: token}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

