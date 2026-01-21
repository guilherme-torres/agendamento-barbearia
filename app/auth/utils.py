from datetime import datetime, timedelta
from typing import Annotated, List
from zoneinfo import ZoneInfo
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from jwt import DecodeError, encode, decode, ExpiredSignatureError
from app.config import get_settings
from app.users.repository import UserRepository
from app.users.schemas import UserResponseDTO


password_hash = PasswordHash.recommended()

def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return password_hash.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded = encode(to_encode, get_settings().JWT_SECRET_KEY, algorithm=get_settings().JWT_ALGORITHM)
    return encoded

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        hours=get_settings().REFRESH_TOKEN_EXPIRE_HOURS
    )
    to_encode.update({"exp": expire})
    encoded = encode(to_encode, get_settings().JWT_SECRET_KEY, algorithm=get_settings().JWT_ALGORITHM)
    return encoded

def decode_jwt(token: str):
    decoded = decode(token, get_settings().JWT_SECRET_KEY, algorithms=[get_settings().JWT_ALGORITHM])
    return decoded

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user_repo = UserRepository()
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt(token)
        email = payload.get("sub")
        if not email:
            raise credentials_exception
    except DecodeError as e:
        raise credentials_exception
    except ExpiredSignatureError as e:
        raise credentials_exception
    user = await user_repo.get_by_email(email)
    if not user:
        raise credentials_exception
    return UserResponseDTO.model_validate(user)


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, current_user: UserResponseDTO = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(403, "acesso negado")
        return current_user