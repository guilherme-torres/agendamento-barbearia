from typing import List
from fastapi import APIRouter, Depends
from app.schedules.dependencies import get_schedule_service
from app.schedules.schemas import ScheduleCreateDTO, ScheduleResponseDTO, ScheduleUpdateDTO
from app.schedules.service import ScheduleService


router = APIRouter(prefix="/schedules")

@router.post("/", response_model=ScheduleResponseDTO)
async def create_schedule(
    data: ScheduleCreateDTO,
    service: ScheduleService = Depends(get_schedule_service)
):
    return await service.create(data)

@router.get("/", response_model=List[ScheduleResponseDTO])
async def list_schedules(service: ScheduleService = Depends(get_schedule_service)):
    return await service.get_all()

@router.get("/{id}", response_model=ScheduleResponseDTO)
async def get_schedule(id: int, service: ScheduleService = Depends(get_schedule_service)):
    return await service.get(id)

@router.patch("/{id}", response_model=ScheduleResponseDTO)
async def update_schedule(
    id: int,
    data: ScheduleUpdateDTO,
    service: ScheduleService = Depends(get_schedule_service)
):
    return await service.update(id, data)

@router.delete("/{id}")
async def delete_schedule(id: int, service: ScheduleService = Depends(get_schedule_service)):
    return await service.delete(id)