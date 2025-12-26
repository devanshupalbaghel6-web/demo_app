"""
User API Routes

This module defines the API endpoints for user management.
It handles user registration, retrieval, and profile access.
"""

# Import FastAPI components
from fastapi import APIRouter, Depends, HTTPException
# Import AsyncSession for database interaction
from sqlalchemy.ext.asyncio import AsyncSession
# Import List for type hinting
from typing import List
# Import database dependency
from core.database import get_db
# Import authentication dependency
from core.deps import get_current_user
# Import Pydantic schemas
from schemas.user import User, UserCreate
# Import service logic
from services import user as user_service
# Import UUID for ID handling
from uuid import UUID

# Initialize the API router for users
router = APIRouter(
    prefix="/users", # All endpoints start with /users
    tags=["users"]   # Grouping tag for documentation
)

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get the current authenticated user's profile.

    Args:
        current_user (User): The authenticated user object, injected by the get_current_user dependency.

    Returns:
        User: The profile data of the logged-in user.
    """
    return current_user

@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.

    Args:
        user (UserCreate): The registration data (email, password).
        db (AsyncSession): The database session dependency.

    Returns:
        User: The newly created user object (excluding password).

    Raises:
        HTTPException: 400 error if the email is already registered.
    """
    # Check if a user with the same email already exists
    db_user = await user_service.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create the new user
    return await user_service.create_user(db, user)

@router.get("/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of users with pagination.
    
    Note: In a production environment, this endpoint should be restricted to administrators.

    Args:
        skip (int): The number of records to skip. Defaults to 0.
        limit (int): The maximum number of records to return. Defaults to 100.
        db (AsyncSession): The database session dependency.

    Returns:
        List[User]: A list of user objects.
    """
    return await user_service.get_users(db, skip, limit)

@router.get("/{user_id}", response_model=User)
async def read_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a specific user by their unique ID.

    Args:
        user_id (UUID): The unique identifier of the user.
        db (AsyncSession): The database session dependency.

    Returns:
        User: The requested user object.

    Raises:
        HTTPException: 404 error if the user is not found.
    """
    db_user = await user_service.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
