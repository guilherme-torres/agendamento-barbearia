from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    BARBER = "barber"
    CLIENT = "client"

@dataclass
class User:
    id: int
    first_name: str
    last_name: str
    email: str
    password_hash: str
    role: UserRole
    phone: str
    created_at: datetime
    updated_at: datetime