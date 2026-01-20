from datetime import time, timedelta
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ScheduleBase(BaseModel):
    day_of_week: int
    start_time: time
    end_time: time
    break_start: Optional[time]
    break_end: Optional[time]


class ScheduleCreateDTO(ScheduleBase):
    tolerance: timedelta = timedelta()


class ScheduleResponseDTO(ScheduleBase):
    id: int
    barber_id: int
    tolerance: timedelta

    model_config = ConfigDict(from_attributes=True)


class ScheduleUpdateDTO(BaseModel):
    day_of_week: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    break_start: Optional[time] = None
    break_end: Optional[time] = None
