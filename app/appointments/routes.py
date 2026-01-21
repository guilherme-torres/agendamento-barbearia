from typing import Annotated, List
from fastapi import APIRouter, Depends
from app.appointments.dependencies import get_appointment_service
from app.appointments.schemas import AppointmentCreateDTO, AppointmentResponseDTO, AppointmentUpdateDTO
from app.appointments.service import AppointmentService
from app.auth.utils import RoleChecker, get_current_user
from app.users.schemas import UserResponseDTO


router = APIRouter(prefix="/appointments", tags=["Appointments"])

ClientOnly = Annotated[UserResponseDTO, Depends(RoleChecker(["client"]))]
BarberOnly = Annotated[UserResponseDTO, Depends(RoleChecker(["barber"]))]
CurrentUser = Annotated[UserResponseDTO, Depends(get_current_user)]

Service = Annotated[AppointmentService, Depends(get_appointment_service)]

@router.post("/", response_model=AppointmentResponseDTO)
async def create_appointment(
    data: AppointmentCreateDTO,
    service: Service,
    current_user: ClientOnly,
):
    return await service.create(data, current_user.id)

@router.get("/", response_model=List[AppointmentResponseDTO])
async def list_appointments(service: Service):
    return await service.get_all()

@router.get("/{id}", response_model=AppointmentResponseDTO)
async def get_appointment(id: int, service: Service):
    return await service.get(id)

@router.patch("/{id}", response_model=AppointmentResponseDTO)
async def update_appointment(
    id: int,
    data: AppointmentUpdateDTO,
    service: Service
):
    return await service.update(id, data)

@router.delete("/{id}")
async def delete_appointment(id: int, service: Service):
    return await service.delete(id)