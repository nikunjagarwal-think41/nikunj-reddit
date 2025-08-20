from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class User(UserBase):
    id: int
    avatar_url: Optional[str] = None
    karma: int
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)
