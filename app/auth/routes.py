from typing import Annotated, Tuple
from fastapi import APIRouter, Depends
from app.auth.dependencies import get_auth_service
from app.auth.schemas import LoginDTO
from app.auth.service import AuthService
from app.auth.utils import get_current_user_with_token
from app.users.schemas import UserResponseDTO


router = APIRouter(prefix="/auth", tags=["Auth"])

Service = Annotated[AuthService, Depends(get_auth_service)]
UserAndToken = Annotated[Tuple[UserResponseDTO, str], Depends(get_current_user_with_token)]

@router.post("/login")
async def login(data: LoginDTO, service: Service):
    return await service.login(data)

@router.post("/revoke")
async def revoke(user_and_token: UserAndToken, service: Service):
    _, token = user_and_token
    return await service.revoke_token(token)