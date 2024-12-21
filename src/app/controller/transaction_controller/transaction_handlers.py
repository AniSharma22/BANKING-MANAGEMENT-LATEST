import uuid

from flask import request
from pydantic.v1 import UUID4
from starlette import status

from src.app.models.request_objects import CreateTransactionRequest
from src.app.models.response import error_response, success_response
from src.app.models.transaction import Transaction
from src.app.services.transaction_service import TransactionService
from fastapi import Request

from src.app.utils.errors.custom_error_codes import INVALID_TRANSACTION_TYPE_ERROR, DATABASE_ERROR, UNEXPECTED_ERROR, \
    ACCOUNT_NOT_EXISTS_ERROR, OPERATION_NOT_PERMITTED_ERROR, INVALID_UUID_ERROR, FIELD_MISSING_ERROR
from src.app.utils.errors.error import InvalidTransactionTypeError, InvalidOperationError, NotExistsError, \
    AccountNotExistsError, FieldMissingError, DatabaseError
from src.app.utils.types import TransactionType
from src.app.utils.utils import Utils
from src.app.utils.validators.validators import Validators


class TransactionHandler:

    def __init__(self, transaction_service: TransactionService):
        self.transaction_service = transaction_service

    async def create_transaction(self, ctx: Request, request: CreateTransactionRequest, transaction_type: str):
        try:
            #:Todo FB :- CONVERT TO AN OBJECT
            # fix value error (exception handling) custom exceptions

            user_id = Utils.get_user_from_context(ctx).get('user_id')

            if transaction_type not in TransactionType.__members__:
                raise InvalidTransactionTypeError(
                    f"Invalid transaction type. Valid types are: {', '.join(TransactionType.__members__.keys())}")

            transaction = Transaction(request.amount, TransactionType[transaction_type].value, str(request.sender_acc_id),
                                      str(request.receiver_acc_id))
            self.transaction_service.create_transaction(transaction, user_id)

            return success_response(
                message="Transaction created successfully.",
            )

        except InvalidTransactionTypeError as e:
            return error_response(
                error_code=INVALID_TRANSACTION_TYPE_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e)
            )
        except FieldMissingError as e:
            return error_response(
                error_code=FIELD_MISSING_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e)
            )
        except InvalidOperationError as e:
            return error_response(
                error_code=OPERATION_NOT_PERMITTED_ERROR,
                status_code=status.HTTP_401_UNAUTHORIZED,
                message=str(e)
            )
        except AccountNotExistsError as e:
            return error_response(
                error_code=ACCOUNT_NOT_EXISTS_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e)
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

    async def view_transaction(self, ctx: Request, account_id: uuid.UUID):
        try:
            user_id = Utils.get_user_from_context(ctx).get('user_id')

            Validators.is_valid_uuid(account_id)

            transactions = self.transaction_service.view_transactions(user_id, str(account_id))
            return success_response(
                message="Transactions fetched successfully.",
                data={"transactions": [transaction.__dict__ for transaction in transactions] if transactions else []}
            )

        except ValueError as e:
            return error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=INVALID_UUID_ERROR,
                message=str(e)
            )
        except InvalidOperationError as e:
            return error_response(
                error_code=OPERATION_NOT_PERMITTED_ERROR,
                status_code=status.HTTP_401_UNAUTHORIZED,
                message=str(e)
            )
        except AccountNotExistsError as e:
            return error_response(
                error_code=ACCOUNT_NOT_EXISTS_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e)
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
