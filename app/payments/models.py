from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class PaymentMethod(str, Enum):
    PIX = "pix"
    DEBIT = "debit"
    CREDIT = "credit"
    CASH = "cash"

@dataclass
class Payment:
    id: int
    appointment_id: int
    amount: float
    method: PaymentMethod
    paid_at: datetime