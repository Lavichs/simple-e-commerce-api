from fastapi import APIRouter
from src.api_v1.routes.products import router as product_router
from src.api_v1.routes.users import router as user_router

router = APIRouter(prefix="/api/v1")

router.include_router(product_router)
router.include_router(user_router)
