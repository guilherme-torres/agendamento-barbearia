from typing import Annotated
from fastapi import Depends
from app.appointments.repository import AppointmentRepository
from app.appointments.service import AppointmentService
from app.catalog_items.dependencies import get_catalog_item_repo
from app.catalog_items.repository import CatalogItemRepository
from app.schedules.dependencies import get_schedule_repo
from app.schedules.repository import ScheduleRepository


def get_appointment_repo():
    return AppointmentRepository()

def get_appointment_service(
    appointment_repo: Annotated[AppointmentRepository, Depends(get_appointment_repo)],
    schedule_repo: Annotated[ScheduleRepository, Depends(get_schedule_repo)],
    catalog_item_repo: Annotated[CatalogItemRepository, Depends(get_catalog_item_repo)],
):
    return AppointmentService(appointment_repo, schedule_repo, catalog_item_repo)