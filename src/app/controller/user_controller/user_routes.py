from fastapi import APIRouter, Depends

from src.app.controller.user_controller.user_handlers import UserHandler
from src.app.models.request_objects import LoginRequest, SignupRequest
from src.app.services.user_service import UserService


def create_user_router(user_service: UserService) -> APIRouter:
    user_router = APIRouter(tags=["user"], prefix="/users")

    user_handler = UserHandler(user_service)



    @user_router.post("/login")
    async def login(request: LoginRequest):
        return await user_handler.login(request)



    @user_router.post("/signup")
    async def signup(request: SignupRequest):
        return await user_handler.signup(request)

    return user_router
