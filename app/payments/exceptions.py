from app.exceptions import AppBaseException


class PaymentNotFound(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Pagamento não encontrado",
            error_code="payment_not_found",
            status_code=404
        )