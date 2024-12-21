import uuid

from fastapi import APIRouter, Depends, Request
from pydantic.v1 import UUID4

from src.app.controller.transaction_controller.transaction_handlers import TransactionHandler
from src.app.middleware.middleware import auth_middleware
from src.app.models.request_objects import CreateTransactionRequest
from src.app.services.transaction_service import TransactionService


def create_transaction_router(transaction_service: TransactionService) -> APIRouter:
    transaction_router = APIRouter(tags=["transactions"], prefix="/transactions")

    transaction_handler = TransactionHandler(transaction_service)

    transaction_router.dependencies = [Depends(auth_middleware)]

    @transaction_router.post("")
    async def create_transaction(ctx: Request, request: CreateTransactionRequest, transaction_type: str):
        return await transaction_handler.create_transaction(ctx, request, transaction_type)

    @transaction_router.get("")
    async def get_transactions(ctx: Request, account_id: uuid.UUID):
        return await transaction_handler.view_transaction(ctx, account_id)

    return transaction_router
