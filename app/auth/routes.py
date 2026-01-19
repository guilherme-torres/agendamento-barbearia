from fastapi import APIRouter, Depends
from app.auth.dependencies import get_auth_service
from app.auth.schemas import LoginDTO
from app.auth.service import AuthService


router = APIRouter(prefix="/auth")

@router.post("/login")
async def login(data: LoginDTO, service: AuthService = Depends(get_auth_service)):
    return await service.login(data)