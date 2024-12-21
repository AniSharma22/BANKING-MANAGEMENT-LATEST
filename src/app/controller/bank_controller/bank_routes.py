import uuid

from fastapi import APIRouter, Depends, Request
from pydantic.v1 import UUID4

from src.app.controller.bank_controller.bank_handlers import BankHandler
from src.app.middleware.middleware import auth_middleware
from src.app.models.request_objects import CreateBankRequest
from src.app.services.bank_service import BankService


def create_bank_router(bank_service: BankService):
    bank_router = APIRouter(tags=["bank"], prefix="/banks")

    bank_handler = BankHandler(bank_service)

    bank_router.dependencies = [Depends(auth_middleware)]

    @bank_router.get("")
    async def get_all_banks():
        return await bank_handler.get_all_banks()

    @bank_router.get("/me")
    async def get_user_banks(ctx: Request):
        return await bank_handler.get_user_banks(ctx)

    @bank_router.get('/available')
    async def get_available_banks(ctx: Request):
        return await bank_handler.get_available_banks_for_user(ctx)

    @bank_router.delete("/{bank_id}")
    async def delete_bank(ctx: Request, bank_id: uuid.UUID):
        return await bank_handler.delete_bank(ctx, bank_id)

    @bank_router.patch("/{bank_id}")
    async def update_bank(ctx: Request, bank_id: uuid.UUID, new_bank_name: str):
        return await bank_handler.update_bank(ctx, bank_id, new_bank_name)

    @bank_router.post("")
    async def create_bank(ctx: Request, request: CreateBankRequest):
        return await bank_handler.create_bank(ctx, request)

    # bank_routes_blueprint.add_url_rule(
    #     '',
    #     'all_banks',
    #     bank_handler.get_all_banks,
    #     methods=['GET']
    # )
    # bank_routes_blueprint.add_url_rule(
    #     '',
    #     'create_bank',
    #     bank_handler.create_bank,
    #     methods=['POST']
    # )

    #
    # bank_routes_blueprint.add_url_rule(
    #     '/me',
    #     'user_banks',
    #     bank_handler.get_user_banks,
    #     methods=['GET']
    # )

    # bank_routes_blueprint.add_url_rule(
    #     '/available',
    #     'available_banks',
    #     bank_handler.get_available_banks_for_user,
    #     methods=['GET']
    # )

    # bank_routes_blueprint.add_url_rule(
    #     '/<bank_id>',
    #     'delete_bank',
    #     bank_handler.delete_bank,
    #     methods=['DELETE']
    # )

    # bank_routes_blueprint.add_url_rule(
    #     '/<bank_id>',
    #     'update_bank',
    #     bank_handler.update_bank,
    #     methods=['PATCH']
    # )

    return bank_router
