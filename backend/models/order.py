"""
Order Database Models

This module defines the SQLAlchemy models for 'orders' and 'order_items'.
It handles the structure of order data, including the relationship between orders, users, and products.
"""

# Import SQLAlchemy types
from sqlalchemy import Column, String, ForeignKey, DateTime, Float, Integer
# Import PostgreSQL UUID type
from sqlalchemy.dialects.postgresql import UUID
# Import relationship for ORM
from sqlalchemy.orm import relationship
# Import SQL functions (like now())
from sqlalchemy.sql import func
# Import uuid for ID generation
import uuid
# Import shared Base class
from models.base import Base

class Order(Base):
    """
    Order Model
    
    Represents a purchase made by a user.
    It acts as a container for multiple OrderItems.
    
    Attributes:
        id (UUID): Unique identifier for the order.
        user_id (UUID): Foreign key referencing the User who placed the order.
        status (str): The current state of the order (e.g., 'pending', 'completed').
        created_at (datetime): Timestamp of when the order was created.
        user (User): Relationship to the User model.
        items (list[OrderItem]): Relationship to the OrderItem model.
    """
    __tablename__ = "orders"

    # Primary Key: UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign Key to User (also UUID)
    # Links this order to a specific row in the 'users' table.
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Order status: 'pending', 'completed', 'cancelled'
    # Defaults to 'pending' but logic in services/order.py might override this.
    status = Column(String, default="pending") 
    
    # Timestamp for when the order was placed
    # server_default=func.now() ensures the database sets this timestamp on insertion.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    # back_populates ensures bidirectional navigation between User and Order.
    user = relationship("User", back_populates="orders")
    
    # cascade="all, delete-orphan" ensures that if an Order is deleted, 
    # all its associated OrderItems are also deleted to prevent orphaned records.
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    """
    OrderItem Model
    
    Represents a specific product and quantity within an order.
    This is effectively a join table between Orders and Products with additional metadata (quantity, price).
    
    Attributes:
        id (UUID): Unique identifier for the order item.
        order_id (UUID): Foreign key referencing the parent Order.
        product_id (UUID): Foreign key referencing the Product.
        quantity (int): The number of units of the product ordered.
        price_at_purchase (float): The price of the product at the moment the order was placed.
        order (Order): Relationship to the parent Order.
        product (Product): Relationship to the Product.
    """
    __tablename__ = "order_items"

    # Primary Key: UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign Keys (UUIDs)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    
    # Quantity of the product ordered
    quantity = Column(Integer, default=1)
    
    # Store price at time of purchase to preserve history.
    # This is crucial because the product's base price might change later, 
    # but the order history should reflect what was actually paid.
    price_at_purchase = Column(Float) 
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
