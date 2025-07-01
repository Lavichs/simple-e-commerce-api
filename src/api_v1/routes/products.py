import uuid

from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.api_v1.dependencies import products_service
from src.schemas.products import SProductAdd, SProduct
from src.services.products import ProductsService

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.post("", status_code=201)
async def add_products(
        product: Annotated[SProductAdd, Depends()],
        product_service: Annotated[ProductsService, Depends(products_service)]
) -> SProduct:
    product = await product_service.add(product)
    return product


@router.get("")
async def get_all_products(
        product_service: Annotated[ProductsService, Depends(products_service)]
) -> list[SProduct]:
    products = await product_service.get_all()
    return products


@router.get("/{id}")
async def get_product_by_id(
        id: uuid.UUID,
        product_service: Annotated[ProductsService, Depends(products_service)]
) -> SProduct:
    product = await product_service.get_by_id(id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{id}")
async def update_product(
        id: uuid.UUID,
        product: Annotated[SProductAdd, Depends()],
        product_service: Annotated[ProductsService, Depends(products_service)]
) -> SProduct:
    product = await product_service.update(id, product)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{id}", status_code=204)
async def delete_product(
        id: uuid.UUID,
        product_service: Annotated[ProductsService, Depends(products_service)]
):
    await product_service.delete(id)

