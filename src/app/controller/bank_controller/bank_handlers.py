import uuid

from pydantic.v1 import UUID4
from starlette import status

from src.app.models.bank import Bank
from src.app.models.request_objects import CreateBankRequest
from src.app.models.response import success_response, error_response
from src.app.services.bank_service import BankService
from src.app.utils.errors.custom_error_codes import DATABASE_ERROR, UNEXPECTED_ERROR, INVALID_UUID_ERROR, \
    BANK_NOT_EXISTS_ERROR
from src.app.utils.errors.error import DatabaseError, BankNotExistsError
from src.app.utils.utils import Utils
from fastapi import Request

from src.app.utils.validators.validators import Validators


class BankHandler:
    def __init__(self, bank_service: BankService):
        self.bank_service = bank_service

    @Utils.admin
    async def create_bank(self, ctx: Request, request: CreateBankRequest):
        try:
            new_bank = Bank(name=request.bank_name)

            self.bank_service.create_new_bank(new_bank)
            return success_response(
                message='Bank created successfully',
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
    async def update_bank(self, ctx: Request, bank_id: uuid.UUID, new_bank_name: str):
        try:
            Validators.is_valid_uuid(bank_id)

            if not new_bank_name or not isinstance(new_bank_name, str):
                raise ValueError("bank name should be a string and not empty")

            self.bank_service.update_bank(str(bank_id), new_bank_name)
            return success_response(
                message='Bank updated successfully',
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

    @Utils.admin
    async def delete_bank(self, ctx: Request, bank_id: uuid.UUID):
        try:
            Validators.is_valid_uuid(bank_id)

            self.bank_service.delete_bank(str(bank_id))
            return success_response(
                message='Bank deleted successfully'
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

    async def get_all_banks(self):
        try:
            banks = self.bank_service.get_all_banks()
            return success_response(
                message="Banks retrieved successfully",
                data={
                    "banks":
                        [bank.__dict__ for bank in banks]
                        if banks else []
                }
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

    async def get_user_banks(self, ctx: Request):
        try:
            user_id = Utils.get_user_from_context(ctx).get('user_id')

            banks = self.bank_service.get_user_banks(user_id)
            return success_response(
                message="Banks retrieved successfully",
                data={
                    "banks": [bank.__dict__ for bank in banks] if banks else []
                }
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

    async def get_available_banks_for_user(self, ctx: Request):
        try:
            user_id = Utils.get_user_from_context(ctx).get('user_id')
            banks = self.bank_service.get_available_banks_for_user(user_id)
            return success_response(
                message="User Banks retrieved successfully",
                data={
                    "banks": [bank.__dict__ for bank in banks] if banks else []
                }
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
