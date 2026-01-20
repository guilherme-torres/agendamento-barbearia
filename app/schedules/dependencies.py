from typing import Annotated
from fastapi import Depends
from app.schedules.repository import ScheduleRepository
from app.schedules.service import ScheduleService


def get_schedule_repo():
    return ScheduleRepository()

def get_schedule_service(schedule_repo: Annotated[ScheduleRepository, Depends(get_schedule_repo)]):
    return ScheduleService(schedule_repo)