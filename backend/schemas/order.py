"""
Order Pydantic Schemas

This module defines the Pydantic models used for validating order data
and serializing order responses. It handles nested structures for order items.
"""

# Import Pydantic components
from pydantic import BaseModel, ConfigDict
# Import List for type hinting lists of objects
from typing import List
# Import datetime for timestamp fields
from datetime import datetime
# Import UUID for unique identifiers
from uuid import UUID

class OrderItemBase(BaseModel):
    """
    Base Order Item Schema
    
    Contains the fundamental data required to identify a product and its quantity within an order.
    
    Attributes:
        product_id (UUID): The unique identifier of the product being ordered.
        quantity (int): The number of units of the product.
    """
    product_id: UUID
    quantity: int

class OrderItemCreate(OrderItemBase):
    """
    Order Item Creation Schema
    
    Used when a user submits a new order. Inherits from OrderItemBase.
    """
    pass

class OrderItem(OrderItemBase):
    """
    Order Item Response Schema
    
    Represents an item within a retrieved order.
    Includes system-generated fields and historical price data.
    
    Attributes:
        id (UUID): The unique identifier of the order item record.
        order_id (UUID): The ID of the parent order.
        price_at_purchase (float): The price of the product when the order was placed.
    """
    id: UUID
    order_id: UUID
    price_at_purchase: float

    # Pydantic V2 Configuration
    # Enables ORM mode for compatibility with SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)

class OrderBase(BaseModel):
    """
    Base Order Schema
    
    Currently empty as there are no shared fields between creation and response 
    that aren't handled by specific logic (like status or user_id).
    """
    pass

class OrderCreate(OrderBase):
    """
    Order Creation Schema
    
    The payload expected when creating a new order.
    
    Attributes:
        items (List[OrderItemCreate]): A list of products and quantities to order.
    """
    items: List[OrderItemCreate]

class Order(OrderBase):
    """
    Order Response Schema
    
    The full representation of an order returned to the client.
    
    Attributes:
        id (UUID): The unique identifier of the order.
        user_id (UUID): The ID of the user who placed the order.
        status (str): The current status of the order (e.g., 'pending', 'completed').
        created_at (datetime): The timestamp when the order was created.
        items (List[OrderItem]): A list of items contained in this order.
    """
    id: UUID
    user_id: UUID
    status: str
    created_at: datetime
    items: List[OrderItem] = []

    # Pydantic V2 Configuration
    # Enables ORM mode for compatibility with SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)
