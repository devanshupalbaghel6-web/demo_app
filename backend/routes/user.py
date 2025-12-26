from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.database import get_db
from core.deps import get_current_user
from schemas.user import User, UserCreate
from services import user as user_service
from uuid import UUID

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get the current authenticated user.
    """
    return current_user

@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.
    
    - **user**: The user registration details.
    """
    db_user = await user_service.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await user_service.create_user(db, user)

@router.get("/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of users.
    
    - **skip**: Number of users to skip.
    - **limit**: Maximum number of users to return.
    """
    return await user_service.get_users(db, skip, limit)

@router.get("/{user_id}", response_model=User)
async def read_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a specific user by ID.
    
    - **user_id**: The UUID of the user.
    """
    db_user = await user_service.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
