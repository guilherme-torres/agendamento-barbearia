from app.payments.exceptions import PaymentNotFound
from app.payments.repository import PaymentRepository
from app.payments.schemas import PaymentCreateDTO, PaymentResponseDTO, PaymentUpdateDTO


class PaymentService:
    def __init__(self, payment_repo: PaymentRepository):
        self.payment_repo = payment_repo
    
    async def create(self, data: PaymentCreateDTO):
        payment = await self.payment_repo.create(data)
        return PaymentResponseDTO.model_validate(payment)
    
    async def get_all(self):
        payments = await self.payment_repo.get_all()
        return [PaymentResponseDTO.model_validate(payment) for payment in payments]
    
    async def get(self, id: int):
        payment = await self.payment_repo.get(id)
        if not payment:
            raise PaymentNotFound
        return PaymentResponseDTO.model_validate(payment)
    
    async def update(self, id: int, data: PaymentUpdateDTO):
        payment = await self.payment_repo.update(id, data.model_dump(exclude_unset=True))
        if not payment:
            raise PaymentNotFound
        return PaymentResponseDTO.model_validate(payment)

    async def delete(self, id: int):
        payment_id = await self.payment_repo.delete(id)
        if not payment_id:
            raise PaymentNotFound
        return None