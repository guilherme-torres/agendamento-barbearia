from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from app.users.models import UserRole


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str


class UserCreateDTO(UserBase):
    password: str


class UserResponseDTO(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdateDTO(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None