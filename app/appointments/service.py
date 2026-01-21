from fastapi import HTTPException
from app.appointments.repository import AppointmentRepository
from app.appointments.schemas import AppointmentCreateDTO, AppointmentResponseDTO, AppointmentUpdateDTO
from app.catalog_items.repository import CatalogItemRepository
from app.schedules.repository import ScheduleRepository


class AppointmentService:
    def __init__(
        self,
        appointment_repo: AppointmentRepository,
        schedule_repo: ScheduleRepository,
        catalog_item_repo: CatalogItemRepository,
    ):
        self.appointment_repo = appointment_repo
        self.schedule_repo = schedule_repo
        self.catalog_item_repo = catalog_item_repo
    
    async def create(self, data: AppointmentCreateDTO, auth_user_id: int):
        schedules = await self.schedule_repo.get_by_barber_id(data.barber_id)
        if len(schedules) == 0:
            raise HTTPException(404, "horário do barbeiro informado não encontrado")
        schedule_days = list(map(lambda schedule: schedule.day_of_week, schedules))
        if data.appointment_date.weekday() not in schedule_days:
            raise HTTPException(400, "dia da semana não disponível")
        # TODO: validar se tem horário disponível no dia selecionado
        # TODO: validar se o horário não extrapola o end_time + tolerance levando em conta o tempo do serviço
        appointment = await self.appointment_repo.create(data.model_dump(exclude_unset=True))
        return AppointmentResponseDTO.model_validate(appointment)
    
    async def get_all(self):
        appointments = await self.appointment_repo.get_all()
        return [AppointmentResponseDTO.model_validate(appointment) for appointment in appointments]
    
    async def get(self, id: int):
        appointment = await self.appointment_repo.get(id)
        if not appointment:
            raise HTTPException(404, "agendamento não encontrado")
        return AppointmentResponseDTO.model_validate(appointment)
    
    async def update(self, id: int, data: AppointmentUpdateDTO):
        appointment = await self.appointment_repo.update(id, data.model_dump(exclude_unset=True))
        if not appointment:
            raise HTTPException(404, "agendamento não encontrado")
        return AppointmentResponseDTO.model_validate(appointment)

    async def delete(self, id: int):
        appointment_id = await self.appointment_repo.delete(id)
        if not appointment_id:
            raise HTTPException(404, "agendamento não encontrado")
        return None