from sqlalchemy import Column, String, ForeignKey, DateTime, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from models.base import Base

class Order(Base):
    """
    Order Model
    
    Represents a purchase made by a user.
    Tracks the status (pending, completed) and when it was created.
    """
    __tablename__ = "orders"

    # Primary Key: UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign Key to User (also UUID)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Order status: 'pending', 'completed', 'cancelled'
    status = Column(String, default="pending") 
    
    # Timestamp for when the order was placed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    """
    OrderItem Model
    
    Represents a specific product and quantity within an order.
    Links Orders and Products (Many-to-Many relationship with extra data).
    """
    __tablename__ = "order_items"

    # Primary Key: UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign Keys (UUIDs)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    
    quantity = Column(Integer, default=1)
    price_at_purchase = Column(Float) # Store price at time of purchase to preserve history
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
