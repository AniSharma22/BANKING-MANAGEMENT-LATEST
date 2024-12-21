from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse
from typing import Any, Optional, Dict, Union, List, Sequence


class SuccessResponse(BaseModel):
    message: str
    data: Optional[Any] = None

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        data = super().model_dump(**kwargs)
        return {k: v for k, v in data.items() if v is not None}


def success_response(
        message: str,
        data: Optional[Any] = None,
        status_code: int = status.HTTP_200_OK,
) -> JSONResponse:
    success_response_obj = SuccessResponse(message=message, data=data)
    return JSONResponse(
        status_code=status_code,
        content=success_response_obj.model_dump(exclude_none=True),
    )


class ErrorResponse(BaseModel):
    message: str
    error_code: int


def error_response(
        message: Any,
        error_code: int,
        status_code: int = status.HTTP_400_BAD_REQUEST,
) -> JSONResponse:
    error_response_obj = ErrorResponse(
        message=message,
        error_code=error_code,
    )
    return JSONResponse(
        status_code=status_code,
        content=error_response_obj.model_dump(),
    )
