from typing import Annotated
from fastapi import Depends
from app.auth.service import AuthService
from app.users.dependencies import get_user_repo
from app.users.repository import UserRepository


def get_auth_service(user_repo: Annotated[UserRepository, Depends(get_user_repo)]):
    return AuthService(user_repo)