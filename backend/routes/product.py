from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.database import get_db
from schemas.product import Product, ProductCreate
from services import product as product_service
from uuid import UUID

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/", response_model=List[Product])
async def get_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of products.
    
    - **skip**: Number of products to skip.
    - **limit**: Maximum number of products to return.
    """
    return await product_service.get_products(db, skip, limit)

@router.post("/", response_model=Product)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new product.
    
    - **product**: The product details.
    """
    return await product_service.create_product(db, product)

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a specific product by ID.
    
    - **product_id**: The UUID of the product.
    """
    product = await product_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=Product)
async def update_product(product_id: UUID, product: ProductCreate, db: AsyncSession = Depends(get_db)):
    updated_product = await product_service.update_product(db, product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    deleted_product = await product_service.delete_product(db, product_id)
    if deleted_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
