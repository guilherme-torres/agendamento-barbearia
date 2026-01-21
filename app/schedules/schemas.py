from datetime import time, timedelta
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, model_validator, Field


class ScheduleBase(BaseModel):
    day_of_week: Annotated[int, Field(ge=0, le=6)]
    start_time: time
    end_time: time
    break_start: Optional[time]
    break_end: Optional[time]


class ScheduleCreateDTO(ScheduleBase):
    tolerance: timedelta = timedelta()

    @model_validator(mode="after")
    def validate_time_fields(self):
        if self.start_time >= self.end_time:
            raise ValueError("O horário de início do turno deve ser anterior ao fim.")

        times = [self.break_start, self.break_end]
        if any(times) and not all(times):
            raise ValueError("Para definir um intervalo, informe tanto o início quanto o fim.")

        if self.break_start and self.break_end:
            if self.break_start >= self.break_end:
                raise ValueError("O início do intervalo deve ser anterior ao fim.")
            if self.break_start <= self.start_time or self.break_end >= self.end_time:
                raise ValueError("O intervalo deve estar contido dentro do horário de trabalho.")

        return self


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
