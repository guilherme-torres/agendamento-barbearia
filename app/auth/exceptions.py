from app.exceptions import AppBaseException


class InvalidCredentials(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Credenciais inválidas",
            error_code="invalid_credentials",
            status_code=400
        )

class AuthError(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Erro durante a autenticação",
            error_code="auth_error",
            status_code=401
        )

class NotPermitted(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Acesso negado",
            error_code="not_permitted",
            status_code=403
        )