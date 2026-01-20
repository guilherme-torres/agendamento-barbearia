from typing import Annotated
from fastapi import Depends
from app.payments.repository import PaymentRepository
from app.payments.service import PaymentService


def get_payment_repo():
    return PaymentRepository()

def get_payment_service(payment_repo: Annotated[PaymentRepository, Depends(get_payment_repo)]):
    return PaymentService(payment_repo)