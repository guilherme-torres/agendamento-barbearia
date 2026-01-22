import time
from app.auth.utils import decode_jwt, get_password_hash, revoke_jwt
from app.users.exceptions import UserAlreadyExists, UserNotFound
from app.users.repository import UserRepository
from app.users.schemas import UserCreateDTO, UserResponseDTO, UserUpdateDTO
from app.utils import redis_client


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create(self, data: UserCreateDTO):
        data: dict = data.model_dump()
        password = data.pop("password")
        data["password_hash"] = get_password_hash(password)
        user = await self.user_repo.create(data)
        if not user:
            raise UserAlreadyExists
        return UserResponseDTO.model_validate(user)
    
    async def get_all(self, limit: int = 100, offset: int = 0):
        users = await self.user_repo.get_all(limit=limit, offset=offset)
        return [UserResponseDTO.model_validate(user) for user in users]
    
    async def get(self, id: int):
        user = await self.user_repo.get(id)
        if not user:
            raise UserNotFound
        return UserResponseDTO.model_validate(user)
    
    async def update(self, id: int, data: UserUpdateDTO):
        user = await self.user_repo.update(id, data.model_dump(exclude_unset=True))
        if not user:
            raise UserNotFound
        return UserResponseDTO.model_validate(user)

    async def delete(self, id: int, token: str):
        user_id = await self.user_repo.delete(id)
        if not user_id:
            raise UserNotFound
        return revoke_jwt(token)