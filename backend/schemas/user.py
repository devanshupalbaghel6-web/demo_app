"""
User Pydantic Schemas

This module defines the Pydantic models used for data validation and serialization
related to User operations (registration, response).
"""

# Import Pydantic's BaseModel and ConfigDict for configuration
from pydantic import BaseModel, ConfigDict
# Import UUID for type hinting
from uuid import UUID

class UserBase(BaseModel):
    """
    Base User Schema
    
    Contains shared properties common to both user creation and user response models.
    
    Attributes:
        email (str): The user's email address.
    """
    email: str

class UserCreate(UserBase):
    """
    User Creation Schema
    
    Defines the data required to register a new user.
    Inherits from UserBase and adds password and admin flag.
    
    Attributes:
        password (str): The raw password provided by the user (will be hashed before storage).
        is_admin (bool): Optional flag to create an admin user. Defaults to False.
    """
    password: str
    is_admin: bool = False

class User(UserBase):
    """
    User Response Schema
    
    Defines the data returned to the client when a user object is requested.
    Inherits from UserBase and adds system-generated fields.
    
    Attributes:
        id (UUID): The unique identifier of the user.
        is_active (bool): Whether the user account is active.
        is_admin (bool): Whether the user has admin privileges.
    """
    id: UUID
    is_active: bool
    is_admin: bool

    # Pydantic V2 Configuration
    # model_config is a dictionary that configures the behavior of the Pydantic model.
    # from_attributes=True (formerly orm_mode=True) tells Pydantic to read data 
    # from attributes of an object (like a SQLAlchemy model) instead of just a dictionary.
    model_config = ConfigDict(from_attributes=True)
