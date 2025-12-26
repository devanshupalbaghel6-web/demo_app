from pydantic import BaseModel
from typing import Optional

# Base schema with common attributes
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None

# Schema for creating a product (same as base for now)
class ProductCreate(ProductBase):
    pass

# Schema for reading a product (includes ID)
class Product(ProductBase):
    id: int

    # Config to allow reading from ORM models
    class Config:
        from_attributes = True
