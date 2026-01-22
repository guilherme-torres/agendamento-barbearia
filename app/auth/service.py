import time
from uuid import uuid4
from app.auth.exceptions import InvalidCredentials
from app.auth.schemas import LoginDTO
from app.auth.utils import create_access_token, create_refresh_token, decode_jwt, revoke_jwt, verify_password
from app.users.repository import UserRepository
from app.utils.redis_client import redis_client


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def login(self, data: LoginDTO):
        user = await self.user_repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise InvalidCredentials
        access_token = create_access_token({
            "sub": user.email,
            "role": user.role,
            "jti": str(uuid4())
        })
        refresh_token = create_refresh_token({
            "sub": user.email,
            "jti": str(uuid4())
        })
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}
    
    async def revoke_token(self, token: str):
        return revoke_jwt(token)