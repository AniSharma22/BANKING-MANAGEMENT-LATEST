from starlette import status

from src.app.models.account import Account
from src.app.models.request_objects import CreateAccountRequest
from src.app.models.response import success_response, error_response
from src.app.services.account_service import AccountService
from fastapi import Request

from src.app.utils.errors.custom_error_codes import DATABASE_ERROR, UNEXPECTED_ERROR, BRANCH_NOT_EXISTS_ERROR, \
    ACCOUNT_EXISTS_ERROR
from src.app.utils.errors.error import DatabaseError, BranchNotExistsError, AccountExistsError
from src.app.utils.utils import Utils


class AccountHandler:

    def __init__(self, account_service: AccountService):
        self.account_service = account_service

    async def create_account(self, ctx: Request, request: CreateAccountRequest):
        try:
            user_id = Utils.get_user_from_context(ctx).get('user_id')

            account = Account(user_id, str(request.branch_id), str(request.bank_id))

            self.account_service.create_new_account(account)
            return success_response(
                message="Account created successfully.",
            )
        except BranchNotExistsError as e:
            return error_response(
                error_code=BRANCH_NOT_EXISTS_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e),
            )
        except AccountExistsError as e:
            return error_response(
                error_code=ACCOUNT_EXISTS_ERROR,
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

    async def get_user_accounts(self, ctx: Request):
        try:
            user_id = Utils.get_user_from_context(ctx).get('user_id')

            accounts = self.account_service.get_user_accounts(user_id)
            return success_response(
                message="Account list retrieved successfully.",
                data={
                    'accounts':
                        [account.__dict__ for account in accounts]
                        if accounts else []
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
