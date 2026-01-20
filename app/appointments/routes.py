from typing import List
from fastapi import APIRouter, Depends
from app.appointments.dependencies import get_appointment_service
from app.appointments.schemas import AppointmentCreateDTO, AppointmentResponseDTO, AppointmentUpdateDTO
from app.appointments.service import AppointmentService


router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=AppointmentResponseDTO)
async def create_appointment(
    data: AppointmentCreateDTO,
    service: AppointmentService = Depends(get_appointment_service)
):
    return await service.create(data)

@router.get("/", response_model=List[AppointmentResponseDTO])
async def list_appointments(service: AppointmentService = Depends(get_appointment_service)):
    return await service.get_all()

@router.get("/{id}", response_model=AppointmentResponseDTO)
async def get_appointment(id: int, service: AppointmentService = Depends(get_appointment_service)):
    return await service.get(id)

@router.patch("/{id}", response_model=AppointmentResponseDTO)
async def update_appointment(
    id: int,
    data: AppointmentUpdateDTO,
    service: AppointmentService = Depends(get_appointment_service)
):
    return await service.update(id, data)

@router.delete("/{id}")
async def delete_appointment(id: int, service: AppointmentService = Depends(get_appointment_service)):
    return await service.delete(id)