from app.exceptions import AppBaseException


class ScheduleAlreadyExists(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Este dia da semana já foi cadastrado",
            error_code="schedule_already_exists",
            status_code=400
        )

class ScheduleNotFound(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Horário não encontrado",
            error_code="schedule_not_found",
            status_code=404
        )

class Forbidden(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Operação proibida",
            error_code="forbidden",
            status_code=403
        )