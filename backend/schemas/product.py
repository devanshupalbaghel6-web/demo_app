"""
Product Pydantic Schemas

This module defines the Pydantic models used for validating product data
during creation and for serializing product data in API responses.
"""

# Import Pydantic components
from pydantic import BaseModel, ConfigDict
# Import Optional for fields that can be None
from typing import Optional
# Import UUID for type hinting
from uuid import UUID

class ProductBase(BaseModel):
    """
    Base Product Schema
    
    Contains the common attributes for a product.
    Used as a base for both creation and response models to avoid duplication.
    
    Attributes:
        name (str): The name of the product.
        description (Optional[str]): A detailed description. Can be None.
        price (float): The cost of the product.
        image_url (Optional[str]): URL to the product image. Can be None.
    """
    name: str
    description: Optional[str] = None
    price: float
    # Image URL is optional, allowing products without images
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    """
    Product Creation Schema
    
    Defines the payload required to create a new product.
    Inherits all fields from ProductBase without modification.
    """
    pass

class Product(ProductBase):
    """
    Product Response Schema
    
    Defines the structure of the product data returned to the client.
    Inherits from ProductBase and adds the database-generated ID.
    
    Attributes:
        id (UUID): The unique identifier of the product.
    """
    id: UUID

    # Pydantic V2 Configuration
    # from_attributes=True enables compatibility with ORM objects (SQLAlchemy models).
    model_config = ConfigDict(from_attributes=True)
