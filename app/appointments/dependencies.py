from fastapi import Depends
from app.appointments.repository import AppointmentRepository
from app.appointments.service import AppointmentService


def get_appointment_repo():
    return AppointmentRepository()

def get_appointment_service(appointment_repo: AppointmentRepository = Depends(get_appointment_repo)):
    return AppointmentService(appointment_repo)