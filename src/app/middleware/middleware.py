from fastapi import HTTPException, Security, Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from src.app.utils.errors.custom_error_codes import INVALID_TOKEN_ERROR, EXPIRED_TOKEN_ERROR, \
    INVALID_TOKEN_PAYLOAD_ERROR
from src.app.utils.utils import Utils



security = HTTPBearer()


def auth_middleware(
        ctx: Request,
        credentials: HTTPAuthorizationCredentials = Security(security)
):
    # Skip auth for login and signup endpoints
    if ctx.url.path in ['/login', '/signup']:
        return None

    try:
        # Get token from credentials
        token = credentials.credentials

        # Decode the token using the secret key
        decoded_token = Utils.decode_jwt_token(token)

        # Extract user_id and role from the decoded token
        user_id = decoded_token.get("user_id")
        role = decoded_token.get("role")

        if not user_id or not role:
            raise HTTPException(
                status_code=401,
                detail={
                    "status_code": INVALID_TOKEN_PAYLOAD_ERROR,
                    "message": "Unauthorized, invalid token payload"
                }
            )

        # Set user data in request context
        user_data = {
            "user_id": user_id,
            "role": role
        }
        Utils.set_user_to_context(ctx, user_data)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail={
                "status_code": EXPIRED_TOKEN_ERROR,
                "message": "Unauthorized, token has expired"
            }
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail={
                "status_code": INVALID_TOKEN_ERROR,
                "message": "Unauthorized, missing or invalid token"
            }
        )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=401,
            detail={
                "status_code": INVALID_TOKEN_ERROR,
                "message": "Unauthorized, missing or invalid token"
            }
        )
