import uuid

from fastapi import APIRouter, Depends, Request

from src.app.controller.branch_controller.branch_handlers import BranchHandler
from src.app.middleware.middleware import auth_middleware
from src.app.models.request_objects import CreateBranchRequest, UpdateBranchRequest
from src.app.services.branch_service import BranchService


def create_branch_router(branch_service: BranchService) -> APIRouter:
    branch_router = APIRouter(tags=["branch"], prefix="/branch")

    branch_handler = BranchHandler(branch_service)

    branch_router.dependencies = [Depends(auth_middleware)]

    @branch_router.post("")
    async def create_branch(ctx: Request, request: CreateBranchRequest):
        return await branch_handler.create_branch(ctx, request)

    @branch_router.put("/{branch_id}")
    async def update_branch(ctx: Request, request: UpdateBranchRequest, branch_id: uuid.UUID):
        return await branch_handler.update_branch(ctx, request, branch_id)

    @branch_router.delete("/{branch_id}")
    async def delete_branch(ctx: Request, branch_id: uuid.UUID):
        return await branch_handler.delete_branch(ctx, branch_id)

    @branch_router.get("/bank/{bank_id}")
    async def get_bank_branches(bank_id: uuid.UUID):
        return await branch_handler.get_bank_branches(bank_id)

    # branch_routes_blueprint.add_url_rule(
    #     '',
    #     'create_branch',
    #     branch_handler.create_branch,
    #     methods=['POST']
    # )
    #
    # branch_routes_blueprint.add_url_rule(
    #     '/<branch_id>',
    #     'update_branch',
    #     branch_handler.update_branch,
    #     methods=['PUT']
    # )
    #
    # branch_routes_blueprint.add_url_rule(
    #     '/<branch_id>',
    #     'delete_branch',
    #     branch_handler.delete_branch,
    #     methods=['DELETE']
    # )
    #
    # branch_routes_blueprint.add_url_rule(
    #     '/bank/<bank_id>',
    #     'get_bank_branches',
    #     branch_handler.get_bank_branches,
    #     methods=['GET']
    # )

    return branch_router
