from datetime import date, datetime, time
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.appointments.models import AppointmentStatus


class AppointmentBase(BaseModel):
    client_id: int
    barber_id: int
    catalog_item_id: int
    appointment_date: date
    appointment_time: time
    status: AppointmentStatus = AppointmentStatus.SCHEDULED


class AppointmentCreateDTO(AppointmentBase):
    pass


class AppointmentResponseDTO(AppointmentBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AppointmentUpdateDTO(BaseModel):
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    status: Optional[AppointmentStatus] = None
    catalog_item_id: Optional[int] = None