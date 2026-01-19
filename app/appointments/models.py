from dataclasses import dataclass
from datetime import date, datetime, time
from enum import Enum


class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    FINISHED = "finished"
    CANCELED = "canceled"

@dataclass
class Appointment:
    id: int
    client_id: int
    barber_id: int
    catalog_item_id: int
    appointment_date: date
    appointment_time: time
    status: AppointmentStatus
    created_at: datetime