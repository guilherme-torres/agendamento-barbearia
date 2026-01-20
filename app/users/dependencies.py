from typing import Annotated
from fastapi import Depends
from app.users.repository import UserRepository
from app.users.service import UserService


def get_user_repo():
    return UserRepository()

def get_user_service(user_repo: Annotated[UserRepository, Depends(get_user_repo)]):
    return UserService(user_repo)