from pydantic import BaseModel, ConfigDict
from uuid import UUID

class UserBase(BaseModel):
    """
    Base User Schema
    
    Shared properties for user creation and reading.
    """
    email: str

class UserCreate(UserBase):
    """
    User Creation Schema
    
    Properties required to create a new user.
    Includes password which is not returned in the response.
    """
    password: str
    is_admin: bool = False

class User(UserBase):
    """
    User Response Schema
    
    Properties returned to the client.
    Includes the generated UUID and status flags.
    """
    id: UUID
    is_active: bool
    is_admin: bool

    # Pydantic V2 Configuration
    # from_attributes=True allows creating Pydantic models from SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)
