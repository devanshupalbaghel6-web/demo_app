"""
Order API Routes

This module defines the API endpoints for managing orders.
It handles the creation and retrieval of orders, ensuring users can only access their own data (in a real app).
"""

# Import FastAPI components
from fastapi import APIRouter, Depends, HTTPException
# Import AsyncSession for database interaction
from sqlalchemy.ext.asyncio import AsyncSession
# Import List for type hinting
from typing import List
# Import database dependency
from core.database import get_db
# Import authentication dependency to get the current user
from core.deps import get_current_user
# Import Pydantic schemas
from schemas.order import Order, OrderCreate
from schemas.user import User
# Import service logic
from services import order as order_service
from services import user as user_service
# Import UUID for ID handling
from uuid import UUID

# Initialize the API router for orders
router = APIRouter(
    tags=["orders"] # Tags for grouping in API documentation
)

@router.post("/orders/", response_model=Order)
async def create_order(order: OrderCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Create a new order for the currently authenticated user.

    Args:
        order (OrderCreate): The order payload containing the list of items.
        current_user (User): The authenticated user (injected by dependency).
        db (AsyncSession): The database session dependency.

    Returns:
        Order: The newly created order object.
    """
    return await order_service.create_order(db, order, current_user.id)

@router.get("/orders/", response_model=List[Order])
async def read_orders(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of all orders in the system.
    
    Note: In a production environment, this endpoint should be restricted to administrators.

    Args:
        skip (int): The number of records to skip. Defaults to 0.
        limit (int): The maximum number of records to return. Defaults to 100.
        db (AsyncSession): The database session dependency.

    Returns:
        List[Order]: A list of all order objects.
    """
    return await order_service.get_orders(db, skip, limit)

@router.get("/users/{user_id}/orders", response_model=List[Order])
async def read_user_orders(user_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Retrieve all orders belonging to a specific user.

    Args:
        user_id (UUID): The unique identifier of the user.
        db (AsyncSession): The database session dependency.

    Returns:
        List[Order]: A list of orders for the specified user.
    """
    return await order_service.get_user_orders(db, user_id)
