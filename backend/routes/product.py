"""
Product API Routes

This module defines the API endpoints for managing products.
It handles HTTP requests for creating, retrieving, and updating products.
"""

# Import FastAPI components
from fastapi import APIRouter, Depends, HTTPException
# Import AsyncSession for database interaction
from sqlalchemy.ext.asyncio import AsyncSession
# Import List for type hinting
from typing import List
# Import database dependency
from core.database import get_db
# Import Pydantic schemas
from schemas.product import Product, ProductCreate
# Import product service logic
from services import product as product_service
# Import UUID for ID handling
from uuid import UUID

# Initialize the API router for products
router = APIRouter(
    prefix="/products", # All endpoints in this router will start with /products
    tags=["products"]   # Tags for grouping in API documentation (Swagger UI)
)

@router.get("/", response_model=List[Product])
async def get_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of products with pagination.

    Args:
        skip (int): The number of records to skip. Defaults to 0.
        limit (int): The maximum number of records to return. Defaults to 100.
        db (AsyncSession): The database session dependency.

    Returns:
        List[Product]: A list of product objects.
    """
    return await product_service.get_products(db, skip, limit)

@router.post("/", response_model=Product)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new product.

    Args:
        product (ProductCreate): The product data payload.
        db (AsyncSession): The database session dependency.

    Returns:
        Product: The created product object.
    """
    return await product_service.create_product(db, product)

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a specific product by its unique ID.

    Args:
        product_id (UUID): The unique identifier of the product.
        db (AsyncSession): The database session dependency.

    Returns:
        Product: The requested product object.

    Raises:
        HTTPException: 404 error if the product is not found.
    """
    product = await product_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=Product)
async def update_product(product_id: UUID, product: ProductCreate, db: AsyncSession = Depends(get_db)):
    """
    Update an existing product.

    Args:
        product_id (UUID): The unique identifier of the product to update.
        product (ProductCreate): The new product data.
        db (AsyncSession): The database session dependency.

    Returns:
        Product: The updated product object.

    Raises:
        HTTPException: 404 error if the product is not found.
    """
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
