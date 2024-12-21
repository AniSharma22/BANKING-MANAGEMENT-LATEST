from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from src.app.utils.errors.custom_error_codes import VALIDATION_ERROR


class InvalidTransactionTypeError(Exception):
    """Raised when transaction type is not in DEPOSIT, WITHDRAW OR TRANSFER"""

    def __init__(self, message: str):
        super().__init__(message)


class UserExistsError(Exception):
    """Raised when attempting to create a user that already exists"""

    def __init__(self, message: str):
        super().__init__(message)


class InvalidCredentialsError(Exception):
    """ Raised when invalid credentials are entered (email or password) """

    def __init__(self, message: str):
        super().__init__(message)


class DatabaseError(Exception):
    """Base exception class for all database-related errors"""

    def __init__(self, message: str):
        super().__init__(message)


class BankNotExistsError(Exception):
    """Raised when bank does not exist"""

    def __init__(self, message: str):
        super().__init__(message)


class BranchNotExistsError(Exception):
    """Raised when branch does not exist"""

    def __init__(self, message: str):
        super().__init__(message)


class AccountExistsError(Exception):
    """Raised when account already exists and user is trying to open another account in same bank"""

    def __init__(self, message: str):
        super().__init__(message)


class AccountNotExistsError(Exception):
    """Raised when account does not exist"""
    def __init__(self, message: str):
        super().__init__(message)


class FieldMissingError(Exception):
    """Raised when some input field is missing and was required"""

    def __init__(self, message: str):
        super().__init__(message)


class InvalidOperationError(Exception):
    """Raise when invalid operations are tried to perform"""

    def __init__(self, message: str):
        super().__init__(message)


def register_validation_exception_handler(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc: RequestValidationError):
        # Customize the response here
        return JSONResponse(
            status_code=422,
            content={
                "error_code": VALIDATION_ERROR,
                "message": "Validation failed",
                "details": exc.errors(),
            },
        )
