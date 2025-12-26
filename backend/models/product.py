"""
Product Database Model

This module defines the SQLAlchemy model for the 'products' table.
It represents the inventory items available for purchase in the e-commerce application.
"""

# Import SQLAlchemy Column types
from sqlalchemy import Column, String, Float, Text
# Import PostgreSQL UUID type
from sqlalchemy.dialects.postgresql import UUID
# Import relationship for ORM associations
from sqlalchemy.orm import relationship
# Import uuid for generating unique IDs
import uuid
# Import the shared Base class
from models.base import Base

class Product(Base):
    """
    Product Model
    
    Represents an item available for sale in the shop.
    
    Attributes:
        id (UUID): The unique identifier for the product.
        name (str): The name of the product. Indexed for search performance.
        description (str): A detailed text description of the product.
        price (float): The price of the product.
        image_url (str): An optional URL pointing to an image of the product.
        order_items (list[OrderItem]): A relationship to the OrderItem model, representing all the times this product has been ordered.
    """
    # Table name in the database
    __tablename__ = "products"

    # Primary Key: UUID
    # Generates a random UUIDv4 if not provided.
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Basic product details
    # name is indexed to allow for faster searching/filtering by product name.
    name = Column(String, index=True)
    
    # Description uses the Text type to allow for longer content than String (VARCHAR).
    description = Column(Text)
    
    # Price is stored as a Float. In a real financial application, 
    # consider using Numeric/Decimal for exact precision to avoid floating point errors.
    price = Column(Float)
    
    # Image URL is optional (nullable=True).
    # This allows products to be created without an image initially.
    image_url = Column(String, nullable=True)

    # Relationship to OrderItem
    # A product can appear in many order items (across different orders).
    # back_populates="product" refers to the 'product' attribute in the OrderItem class.
    order_items = relationship("OrderItem", back_populates="product")
