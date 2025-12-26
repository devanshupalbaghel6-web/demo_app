from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.database import get_db
from core.deps import get_current_user
from schemas.order import Order, OrderCreate
from schemas.user import User
from services import order as order_service
from services import user as user_service
from uuid import UUID

router = APIRouter(
    tags=["orders"]
)

@router.post("/orders/", response_model=Order)
async def create_order(order: OrderCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Create a new order for the current user.
    
    - **order**: The order details (items).
    - **current_user**: The authenticated user creating the order.
    """
    return await order_service.create_order(db, order, current_user.id)

@router.get("/orders/", response_model=List[Order])
async def read_orders(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of orders (Admin only ideally, but open for now).
    
    - **skip**: Number of orders to skip.
    - **limit**: Maximum number of orders to return.
    """
    return await order_service.get_orders(db, skip, limit)

@router.get("/users/{user_id}/orders", response_model=List[Order])
async def read_user_orders(user_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Retrieve all orders for a specific user.
    
    - **user_id**: The UUID of the user.
    """
    return await order_service.get_user_orders(db, user_id)
