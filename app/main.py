from contextlib import asynccontextmanager
from typing import List
from fastapi import Depends, FastAPI
from app.database import pool
from app.users.dependencies import get_user_service
from app.users.schemas import UserCreateDTO, UserResponseDTO, UserUpdateDTO
from app.users.service import UserService


@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.open()
    yield
    await pool.close()

app = FastAPI(lifespan=lifespan)

@app.post("/users", response_model=UserResponseDTO)
async def create_user(
    data: UserCreateDTO,
    service: UserService = Depends(get_user_service)
):
    return await service.create(data)

@app.get("/users", response_model=List[UserResponseDTO])
async def list_users(service: UserService = Depends(get_user_service)):
    return await service.get_all()

@app.get("/users/{id}", response_model=UserResponseDTO)
async def get_user(id: int, service: UserService = Depends(get_user_service)):
    return await service.get(id)

@app.patch("/users/{id}", response_model=UserResponseDTO)
async def update_user(
    id: int,
    data: UserUpdateDTO,
    service: UserService = Depends(get_user_service)
):
    return await service.update(id, data)

@app.delete("/users/{id}")
async def delete_user(id: int, service: UserService = Depends(get_user_service)):
    return await service.delete(id)