from sqlalchemy import Column, String, Float, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from models.base import Base

class Product(Base):
    """
    Product Model
    
    Represents an item available for sale in the shop.
    """
    __tablename__ = "products"

    # Primary Key: UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Basic product details
    name = Column(String, index=True)
    description = Column(Text)
    price = Column(Float)
    
    # Image URL is optional (nullable=True by default in SQLAlchemy if not specified, but explicit is better)
    # This allows products to be created without an image initially.
    image_url = Column(String, nullable=True)

    # Relationship to OrderItem
    # A product can appear in many order items (across different orders).
    order_items = relationship("OrderItem", back_populates="product")
