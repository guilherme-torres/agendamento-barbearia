from app.exceptions import AppBaseException


class UserAlreadyExists(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Usuário já existe",
            error_code="user_already_exists",
            status_code=400
        )

class UserNotFound(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Usuário não encontrado",
            error_code="user_not_found",
            status_code=404
        )