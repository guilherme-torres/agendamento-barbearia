from typing import Annotated, List
from fastapi import APIRouter, Depends
from app.auth.utils import RoleChecker, get_current_user
from app.schedules.dependencies import get_schedule_service
from app.schedules.schemas import ScheduleCreateDTO, ScheduleResponseDTO, ScheduleUpdateDTO
from app.schedules.service import ScheduleService
from app.users.schemas import UserResponseDTO


router = APIRouter(prefix="/schedules", tags=["Schedules"])

ClientOnly = Annotated[UserResponseDTO, Depends(RoleChecker(["client"]))]
BarberOnly = Annotated[UserResponseDTO, Depends(RoleChecker(["barber"]))]
CurrentUser = Annotated[UserResponseDTO, Depends(get_current_user)]

Service = Annotated[ScheduleService, Depends(get_schedule_service)]

@router.post("/", response_model=ScheduleResponseDTO)
async def create_schedule(
    data: ScheduleCreateDTO,
    service: Service,
    current_user: BarberOnly
):
    return await service.create(data, current_user.id)

@router.get("/", response_model=List[ScheduleResponseDTO])
async def list_schedules(service: Service, current_user: CurrentUser):
    return await service.get_all()

@router.get("/{id}", response_model=ScheduleResponseDTO)
async def get_schedule(id: int, service: Service, current_user: CurrentUser):
    return await service.get(id)

@router.patch("/{id}", response_model=ScheduleResponseDTO)
async def update_schedule(
    id: int,
    data: ScheduleUpdateDTO,
    service: Service,
    current_user: BarberOnly
):
    return await service.update(id, data, current_user.id)

@router.delete("/{id}")
async def delete_schedule(id: int, service: Service, current_user: BarberOnly):
    return await service.delete(id, current_user.id)