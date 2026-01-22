from app.schedules.exceptions import Forbidden, ScheduleAlreadyExists, ScheduleNotFound
from app.schedules.repository import ScheduleRepository
from app.schedules.schemas import ScheduleCreateDTO, ScheduleResponseDTO, ScheduleUpdateDTO


class ScheduleService:
    def __init__(self, schedule_repo: ScheduleRepository):
        self.schedule_repo = schedule_repo
    
    async def create(self, data: ScheduleCreateDTO, auth_user_id: int):
        data: dict = data.model_dump()
        data.update({"barber_id": auth_user_id})
        schedule = await self.schedule_repo.create(data)
        if not schedule:
            raise ScheduleAlreadyExists
        return ScheduleResponseDTO.model_validate(schedule)
    
    async def get_all(self):
        schedules = await self.schedule_repo.get_all()
        return [ScheduleResponseDTO.model_validate(schedule) for schedule in schedules]
    
    async def get(self, id: int):
        schedule = await self.schedule_repo.get(id)
        if not schedule:
            raise ScheduleNotFound
        return ScheduleResponseDTO.model_validate(schedule)
    
    async def update(self, id: int, data: ScheduleUpdateDTO, auth_user_id: int):
        schedule = await self.schedule_repo.update(id, data.model_dump(exclude_unset=True))
        if not schedule:
            raise ScheduleNotFound
        if schedule.barber_id != auth_user_id:
            raise Forbidden
        return ScheduleResponseDTO.model_validate(schedule)

    async def delete(self, id: int, auth_user_id: int):
        schedule = await self.schedule_repo.get(id)
        if not schedule:
            raise ScheduleNotFound
        if schedule.barber_id != auth_user_id:
            raise Forbidden
        await self.schedule_repo.delete(id)
        return None