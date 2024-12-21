from starlette import status

from src.app.models.request_objects import LoginRequest, SignupRequest
from src.app.models.response import success_response, error_response
from src.app.models.user import User
from src.app.services.user_service import UserService
from src.app.utils.errors.custom_error_codes import (
    INVALID_CREDENTIALS_ERROR, UNEXPECTED_ERROR, DATABASE_ERROR,
    USER_EXISTS_ERROR
)
from src.app.utils.errors.error import InvalidCredentialsError, UserExistsError, DatabaseError
from src.app.utils.utils import Utils


class UserHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def login(self, request: LoginRequest):
        try:
            user = self.user_service.login_user(request.email.lower(), request.password)
            token = Utils.create_jwt_token(user.id, user.role)
            return success_response(
                message="Login Successful",
                data={"token": token}
            )
        except InvalidCredentialsError as e:
            return error_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                error_code=INVALID_CREDENTIALS_ERROR,
                message=str(e)
            )
        except DatabaseError as e:
            return error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=DATABASE_ERROR,
                message=str(e)
            )
        except Exception as e:
            return error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=UNEXPECTED_ERROR,
                message=str(e)
            )

    async def signup(self, request: SignupRequest):
        try:
            user = User(
                name=request.name,
                email=request.email,
                password=request.password,
                phone_no=request.phone_no,
                address=request.address
            )

            # Assuming signup_user needs to be async as well
            self.user_service.signup_user(user)
            token = Utils.create_jwt_token(user.id, user.role)
            return success_response(
                message="Signup Successful",
                data={'token': token, 'role': user.role}
            )
        except UserExistsError as e:
            return error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=USER_EXISTS_ERROR,
                message=str(e)
            )
        except DatabaseError as e:
            return error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=DATABASE_ERROR,
                message=str(e)
            )
        except Exception as e:
            return error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=UNEXPECTED_ERROR,
                message=str(e)
            )
