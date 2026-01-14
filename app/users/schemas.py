from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.users.models import UserRole


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
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
    phone: str | None = None