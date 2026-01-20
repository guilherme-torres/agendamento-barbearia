from typing import Annotated, List
from fastapi import Depends, Query
from fastapi.routing import APIRouter
from app.auth.utils import RoleChecker, get_current_user
from app.schemas import PaginationOptions
from app.users.dependencies import get_user_service
from app.users.schemas import UserCreateDTO, UserResponseDTO, UserUpdateDTO
from app.users.service import UserService


router = APIRouter(prefix="/users", tags=["Users"])

ClientOnly = Annotated[UserResponseDTO, Depends(RoleChecker(["client"]))]
BarberOnly = Annotated[UserResponseDTO, Depends(RoleChecker(["barber"]))]
CurrentUser = Annotated[UserResponseDTO, Depends(get_current_user)]

Service = Annotated[UserService, Depends(get_user_service)]

@router.post("/", response_model=UserResponseDTO)
async def create_user(data: UserCreateDTO, service: Service):
    return await service.create(data)

@router.get("/barbers", response_model=List[UserResponseDTO])
async def list_barbers(
    service: Service,
    current_user: ClientOnly,
    pagination_options: Annotated[PaginationOptions, Query()]
):
    return await service.list_barbers(
        limit=pagination_options.limit,
        offset=pagination_options.offset
    )

@router.get("/me")
async def get_current_user_info(current_user: CurrentUser):
    return current_user

@router.patch("/me", response_model=UserResponseDTO)
async def update_current_user(
    data: UserUpdateDTO,
    service: Service,
    current_user: CurrentUser,
):
    return await service.update(current_user.id, data)

@router.delete("/me")
async def delete_current_user(service: Service, current_user: CurrentUser):
    return await service.delete(current_user.id)