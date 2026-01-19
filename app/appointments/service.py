from fastapi import HTTPException
from app.appointments.repository import AppointmentRepository
from app.appointments.schemas import AppointmentCreateDTO, AppointmentResponseDTO, AppointmentUpdateDTO


class AppointmentService:
    def __init__(self, appointment_repo: AppointmentRepository):
        self.appointment_repo = appointment_repo
    
    async def create(self, data: AppointmentCreateDTO):
        appointment = await self.appointment_repo.create(data)
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