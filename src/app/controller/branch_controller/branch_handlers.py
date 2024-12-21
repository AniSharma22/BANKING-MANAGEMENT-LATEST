import uuid

from pydantic.v1 import UUID4
from starlette import status

from src.app.models.branch import Branch
from src.app.models.request_objects import CreateBranchRequest, UpdateBranchRequest
from src.app.models.response import success_response, error_response
from src.app.services.branch_service import BranchService
from src.app.utils.errors.custom_error_codes import DATABASE_ERROR, UNEXPECTED_ERROR, BANK_NOT_EXISTS_ERROR, \
    BRANCH_NOT_EXISTS_ERROR, INVALID_UUID_ERROR
from src.app.utils.errors.error import DatabaseError, BankNotExistsError, BranchNotExistsError
from src.app.utils.utils import Utils
from fastapi import Request

from src.app.utils.validators.validators import Validators


class BranchHandler:
    branch_service: BranchService

    def __init__(self, branch_service: BranchService):
        self.branch_service = branch_service

    @Utils.admin
    async def create_branch(self, ctx: Request, request: CreateBranchRequest):
        try:

            new_branch = Branch(
                name=request.branch_name,
                address=request.branch_address,
                bank_id=str(request.bank_id),
            )

            self.branch_service.create_new_branch(new_branch)

            return success_response(
                message="Branch created successfully.",
            )
        except BankNotExistsError as e:
            return error_response(
                error_code=BANK_NOT_EXISTS_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e),
            )
        except DatabaseError as e:
            return error_response(
                error_code=DATABASE_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e)
            )
        except Exception as e:
            return error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=UNEXPECTED_ERROR,
                message=str(e)
            )

    @Utils.admin
    async def update_branch(self, ctx: Request, request: UpdateBranchRequest, branch_id: uuid.UUID):
        try:
            Validators.is_valid_uuid(branch_id)

            self.branch_service.update_branch_details(str(branch_id), request.new_branch_name,
                                                      request.new_branch_address)
            return success_response(
                message="Branch updated successfully.",
            )

        except ValueError as e:
            return error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=INVALID_UUID_ERROR,
                message=str(e)
            )
        except BranchNotExistsError as e:
            return error_response(
                error_code=BRANCH_NOT_EXISTS_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e),
            )

        except DatabaseError as e:
            return error_response(
                error_code=DATABASE_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e)
            )
        except Exception as e:
            return error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=UNEXPECTED_ERROR,
                message=str(e)
            )

    @Utils.admin
    async def delete_branch(self, ctx: Request, branch_id: uuid.UUID):
        try:
            Validators.is_valid_uuid(branch_id)

            self.branch_service.remove_branch(str(branch_id))
            return success_response(
                message="Branch deleted successfully"
            )

        except ValueError as e:
            return error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=INVALID_UUID_ERROR,
                message=str(e)
            )
        except BranchNotExistsError as e:
            return error_response(
                error_code=BRANCH_NOT_EXISTS_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e),
            )
        except DatabaseError as e:
            return error_response(
                error_code=DATABASE_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e)
            )
        except Exception as e:
            return error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=UNEXPECTED_ERROR,
                message=str(e)
            )

    async def get_bank_branches(self, bank_id: uuid.UUID):
        try:
            Validators.is_valid_uuid(bank_id)

            branches = self.branch_service.get_bank_branches(str(bank_id))
            return success_response(
                message="Bank branches fetched successfully.",
                data={"bank_branches": [branch.__dict__ for branch in branches] if branches else []}
            )


        except ValueError as e:
            return error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=INVALID_UUID_ERROR,
                message=str(e)
            )
        except BankNotExistsError as e:
            return error_response(
                error_code=BANK_NOT_EXISTS_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e),
            )
        except DatabaseError as e:
            return error_response(
                error_code=DATABASE_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e)
            )
        except Exception as e:
            return error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=UNEXPECTED_ERROR,
                message=str(e)
            )
