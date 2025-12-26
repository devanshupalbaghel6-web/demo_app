"""
Dependencies Module

This module defines FastAPI dependencies used across the application.
It primarily handles authentication and authorization by providing a dependency
to retrieve the current authenticated user from the JWT token.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.config import settings
from services import user as user_service
from schemas.token import TokenData

# Define the OAuth2 scheme for token retrieval
# This tells FastAPI that the token is retrieved from the "Authorization" header
# and the token URL is "/token"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    """
    Dependency to get the current authenticated user.

    This function:
    1. Retrieves the JWT token from the request header.
    2. Decodes and validates the token using the secret key.
    3. Extracts the user's email (subject) from the token payload.
    4. Fetches the user from the database using the email.
    5. Returns the user object if valid, otherwise raises an HTTP 401 Unauthorized exception.

    Args:
        token (str): The JWT access token.
        db (AsyncSession): The database session.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If the token is invalid, expired, or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # Extract the email (subject) from the payload
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        # Create a TokenData object (for validation/typing)
        token_data = TokenData(email=email)
    except JWTError:
        # Raise exception if token decoding fails
        raise credentials_exception
    
    # Fetch the user from the database
    user = await user_service.get_user_by_email(db, email=token_data.email)
    if user is None:
        # Raise exception if user is not found
        raise credentials_exception
    
    return user
