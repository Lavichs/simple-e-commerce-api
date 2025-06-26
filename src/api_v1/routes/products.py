from fastapi import APIRouter, Depends
from typing import Annotated

from src.api_v1.dependencies import products_service
from src.schemas.products import SProductAdd
from src.services.products import ProductsService

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.post("", status_code=201)
async def add_products(
        product: Annotated[SProductAdd, Depends()],
        product_service: Annotated[ProductsService, Depends(products_service)]
):
    product = await product_service.add(product)
    return product


@router.get("")
async def get_all_products(
        product_service: Annotated[ProductsService, Depends(products_service)]
):
    products = await product_service.get_all()
    return {"data": products}
