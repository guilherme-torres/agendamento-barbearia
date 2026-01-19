from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.payments.models import PaymentMethod


class PaymentBase(BaseModel):
    appointment_id: int
    amount: float
    method: PaymentMethod
    paid_at: datetime


class PaymentCreateDTO(PaymentBase):
    pass


class PaymentResponseDTO(PaymentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PaymentUpdateDTO(BaseModel):
    amount: Optional[float] = None
    method: Optional[PaymentMethod] = None
    paid_at: Optional[datetime] = None