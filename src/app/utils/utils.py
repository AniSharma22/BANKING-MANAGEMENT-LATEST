from functools import wraps

from bcrypt import hashpw, checkpw, gensalt
import asyncio
import jwt as jwt
import datetime
from fastapi import Request
from typing import Optional

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR

from src.app.models.response import error_response
from src.app.utils.errors.custom_error_codes import SYSTEM_ERROR, UNAUTHORIZED_ACCESS_ERROR, INVALID_TOKEN_PAYLOAD_ERROR


class Utils:
    SECRET_KEY = "SECRET"

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.
        """
        return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        """
        Verify a password against a hashed password.
        """
        return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def create_jwt_token(user_id: str, role: str) -> str:
        """
        Generates a JWT token with the provided user_id and role.

        Args:
            user_id (str): The ID of the user.
            role (str): The role of the user (e.g., "admin", "user").

        Returns:
            str: The generated JWT token.
        """
        try:
            # Define the payload
            payload = {
                "user_id": user_id,
                "role": role,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Token expires in 1 hour
                "iat": datetime.datetime.utcnow(),  # Issued at
                "nbf": datetime.datetime.utcnow(),  # Not before
            }

            # Encode the payload with the secret key
            token = jwt.encode(payload, Utils.SECRET_KEY, algorithm="HS256")

            return token
        except Exception as e:
            raise ValueError(f"Failed to generate JWT token: {str(e)}")

    @staticmethod
    def decode_jwt_token(token: str) -> dict:
        return jwt.decode(token, Utils.SECRET_KEY, algorithms=["HS256"])

    @staticmethod
    def admin(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # Get the Request object from args or kwargs
                request = next((arg for arg in args if isinstance(arg, Request)), kwargs.get('request'))

                if not request:
                    return error_response(
                        status_code=HTTP_400_BAD_REQUEST,
                        error_code=INVALID_TOKEN_PAYLOAD_ERROR,
                        message="Request context not available"
                    )

                user = Utils.get_user_from_context(request)
                if not user or user.get('role') != 'admin':
                    return error_response(
                        status_code=HTTP_401_UNAUTHORIZED,
                        error_code=UNAUTHORIZED_ACCESS_ERROR,
                        message="Admin access required"
                    )

                # Handle both async and sync functions
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                return func(*args, **kwargs)

            except Exception as e:
                return error_response(
                    status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                    error_code=SYSTEM_ERROR,
                    message="Error checking admin privileges"
                )

        return wrapper

    @staticmethod
    def get_user_from_context(request: Request) -> Optional[dict]:
        """Get user data from request state"""
        return getattr(request.state, "user", None)

    @staticmethod
    def set_user_to_context(ctx: Request, user_data: dict):
        """Set user data to request state"""
        ctx.state.user = user_data
