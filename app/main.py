from contextlib import asynccontextmanager
from typing import List
from fastapi import Depends, FastAPI
from app.database import get_db, pool
from app.users.dependencies import get_user_service
from app.users.schemas import UserCreateDTO, UserResponseDTO
from app.users.service import UserService
from app.users.tables import create_users_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool.open()
    # create tables
    with get_db() as conn:
        create_users_table(conn)
    yield
    pool.close()

app = FastAPI(lifespan=lifespan)

@app.post("/users", response_model=UserResponseDTO)
def create_user(
    data: UserCreateDTO,
    service: UserService = Depends(get_user_service)
):
    return service.create(data)


@app.get("/users", response_model=List[UserResponseDTO])
def list_users(service: UserService = Depends(get_user_service)):
    return service.get_all()