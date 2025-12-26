from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.database import get_db
from schemas.order import Order, OrderCreate
from services import order as order_service
from services import user as user_service

router = APIRouter(
    tags=["orders"]
)

@router.post("/orders/", response_model=Order)
async def create_order(order: OrderCreate, user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await order_service.create_order(db, order, user_id)

@router.get("/orders/", response_model=List[Order])
async def read_orders(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await order_service.get_orders(db, skip, limit)

@router.get("/users/{user_id}/orders", response_model=List[Order])
async def read_user_orders(user_id: int, db: AsyncSession = Depends(get_db)):
    return await order_service.get_user_orders(db, user_id)
