"""
Token Schemas

This module defines the Pydantic models for JWT tokens.
It includes schemas for the token response and the token payload data.
"""

from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """
    Schema for the authentication token response.

    Attributes:
        access_token (str): The JWT access token string.
        token_type (str): The type of token (e.g., "bearer").
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for the data embedded in the token payload.

    Attributes:
        email (Optional[str]): The email address of the user (subject).
    """
    email: Optional[str] = None
