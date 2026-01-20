from typing import List
from fastapi import APIRouter, Depends
from app.payments.dependencies import get_payment_service
from app.payments.schemas import PaymentCreateDTO, PaymentResponseDTO, PaymentUpdateDTO
from app.payments.service import PaymentService


router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentResponseDTO)
async def create_payment(
    data: PaymentCreateDTO,
    service: PaymentService = Depends(get_payment_service)
):
    return await service.create(data)

@router.get("/", response_model=List[PaymentResponseDTO])
async def list_payments(service: PaymentService = Depends(get_payment_service)):
    return await service.get_all()

@router.get("/{id}", response_model=PaymentResponseDTO)
async def get_payment(id: int, service: PaymentService = Depends(get_payment_service)):
    return await service.get(id)

@router.patch("/{id}", response_model=PaymentResponseDTO)
async def update_payment(
    id: int,
    data: PaymentUpdateDTO,
    service: PaymentService = Depends(get_payment_service)
):
    return await service.update(id, data)

@router.delete("/{id}")
async def delete_payment(id: int, service: PaymentService = Depends(get_payment_service)):
    return await service.delete(id)