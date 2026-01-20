from fastapi import HTTPException
from app.auth.schemas import LoginDTO
from app.auth.utils import create_access_token, create_refresh_token, verify_password
from app.users.repository import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def login(self, data: LoginDTO):
        user = await self.user_repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(400, "credenciais inválidas")
        access_token = create_access_token({"sub": user.email})
        refresh_token = create_refresh_token({"sub": user.email})
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}