from app.exceptions import AppBaseException


class AppointmentNotFound(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Agendamento não encontrado",
            error_code="appointment_not_found",
            status_code=404
        )