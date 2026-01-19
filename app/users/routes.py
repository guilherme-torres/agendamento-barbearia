from typing import List
from fastapi import Depends
from fastapi.routing import APIRouter
from app.users.dependencies import get_user_service
from app.users.schemas import UserCreateDTO, UserResponseDTO, UserUpdateDTO
from app.users.service import UserService


router = APIRouter(prefix="/users")

@router.post("/", response_model=UserResponseDTO)
async def create_user(
    data: UserCreateDTO,
    service: UserService = Depends(get_user_service)
):
    return await service.create(data)

@router.get("/", response_model=List[UserResponseDTO])
async def list_users(service: UserService = Depends(get_user_service)):
    return await service.get_all()

@router.get("/{id}", response_model=UserResponseDTO)
async def get_user(id: int, service: UserService = Depends(get_user_service)):
    return await service.get(id)

@router.patch("/{id}", response_model=UserResponseDTO)
async def update_user(
    id: int,
    data: UserUpdateDTO,
    service: UserService = Depends(get_user_service)
):
    return await service.update(id, data)

@router.delete("/{id}")
async def delete_user(id: int, service: UserService = Depends(get_user_service)):
    return await service.delete(id)