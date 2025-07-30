from fastapi.responses import JSONResponse
from .protocol import ErrorResponse
from typing import Optional

def create_error(
        message: str,
        type: str,
        param: Optional[str] = None,
        code: Optional[str] = None,
        status: int = 500) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content=ErrorResponse(
            error={
                'message': message,
                'type': type,
                'param': param,
                'code': code
            },
        ).model_dump(),
    )

def create_500_error(message: str) -> JSONResponse:
    return create_error(
        message=message,
        type='internal_error',
        code='500 INTERNAL_ERROR',
        status=500,
    )

def create_501_error(func: str) -> JSONResponse:
    return create_error(
        message=f'{func} not implemented',
        type='not_implemented',
        code='501 NOT_IMPLEMENT',
        status=501,
    )


