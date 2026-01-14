from fastapi import HTTPException
from app.users.repository import UserRepository
from app.users.schemas import UserCreateDTO, UserResponseDTO


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create(self, data: UserCreateDTO):
        data: dict = data.model_dump()
        password = data.pop("password")
        data["password_hash"] = password
        user = self.user_repo.create(data)
        if not user:
            raise HTTPException(400, "o usuário com este email já existe")
        return UserResponseDTO.model_validate(user)
    
    def get_all(self):
        users = self.user_repo.get_all()
        return [UserResponseDTO.model_validate(user) for user in users]