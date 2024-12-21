from fastapi import FastAPI, Depends, Request, APIRouter

from src.app.controller.account_controller.account_handlers import AccountHandler
from src.app.middleware.middleware import auth_middleware
from src.app.models.request_objects import CreateAccountRequest
from src.app.services.account_service import AccountService


def create_account_router(account_service: AccountService) -> APIRouter:
    account_router = APIRouter(tags=["account"], prefix="/accounts")

    account_handler = AccountHandler(account_service)

    account_router.dependencies = [Depends(auth_middleware)]

    @account_router.post("")
    async def create_account(ctx: Request, request: CreateAccountRequest):
        return await account_handler.create_account(ctx, request)

    @account_router.get("")
    async def get_accounts(ctx: Request):
        return await account_handler.get_user_accounts(ctx)

    # account_routes_blueprint.add_url_rule(
    #     '',
    #     'create_account',
    #     account_handler.create_account,
    #     methods=['POST']
    # )
    #
    # account_routes_blueprint.add_url_rule(
    #     '',
    #     'get_accounts',
    #     account_handler.get_user_accounts,
    #     methods=['GET']
    # )

    return account_router
