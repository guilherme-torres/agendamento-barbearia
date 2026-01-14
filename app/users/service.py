from fastapi import HTTPException
from app.users.repository import UserRepository
from app.users.schemas import UserCreateDTO, UserResponseDTO, UserUpdateDTO
from app.utils.password_hashing import get_password_hash


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create(self, data: UserCreateDTO):
        data: dict = data.model_dump()
        password = data.pop("password")
        data["password_hash"] = get_password_hash(password)
        user = await self.user_repo.create(data)
        if not user:
            raise HTTPException(400, "um usuário com este email já existe")
        return UserResponseDTO.model_validate(user)
    
    async def get_all(self):
        users = await self.user_repo.get_all()
        return [UserResponseDTO.model_validate(user) for user in users]
    
    async def get(self, id: int):
        user = await self.user_repo.get(id)
        if not user:
            raise HTTPException(404, "usuário não encontrado")
        return UserResponseDTO.model_validate(user)
    
    async def update(self, id: int, data: UserUpdateDTO):
        print(data.model_dump(exclude_unset=True))
        user = await self.user_repo.update(id, data.model_dump(exclude_unset=True))
        if not user:
            raise HTTPException(404, "usuário não encontrado")
        return UserResponseDTO.model_validate(user)

    async def delete(self, id: int):
        user_id = await self.user_repo.delete(id)
        if not user_id:
            raise HTTPException(404, "usuário não encontrado")
        return None