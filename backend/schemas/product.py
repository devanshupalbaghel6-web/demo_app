from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

class ProductBase(BaseModel):
    """
    Base Product Schema
    
    Shared properties for product creation and reading.
    """
    name: str
    description: Optional[str] = None
    price: float
    # Image URL is optional, allowing products without images
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    """
    Product Creation Schema
    
    Inherits all fields from ProductBase.
    """
    pass

class Product(ProductBase):
    """
    Product Response Schema
    
    Includes the unique UUID assigned by the database.
    """
    id: UUID

    # Pydantic V2 Configuration
    model_config = ConfigDict(from_attributes=True)
