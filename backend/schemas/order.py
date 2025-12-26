from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime
from uuid import UUID

class OrderItemBase(BaseModel):
    """
    Base Order Item Schema
    
    Represents a product and its quantity in an order.
    """
    product_id: UUID
    quantity: int

class OrderItemCreate(OrderItemBase):
    """
    Order Item Creation Schema
    """
    pass

class OrderItem(OrderItemBase):
    """
    Order Item Response Schema
    
    Includes the item ID, order ID, and the price at the time of purchase.
    """
    id: UUID
    order_id: UUID
    price_at_purchase: float

    # Pydantic V2 Configuration
    model_config = ConfigDict(from_attributes=True)

class OrderBase(BaseModel):
    """
    Base Order Schema
    """
    pass

class OrderCreate(OrderBase):
    """
    Order Creation Schema
    
    Expects a list of items to include in the order.
    """
    items: List[OrderItemCreate]

class Order(OrderBase):
    """
    Order Response Schema
    
    Includes the order ID, user ID, status, creation timestamp, and the list of items.
    """
    id: UUID
    user_id: UUID
    status: str
    created_at: datetime
    items: List[OrderItem] = []

    # Pydantic V2 Configuration
    model_config = ConfigDict(from_attributes=True)
