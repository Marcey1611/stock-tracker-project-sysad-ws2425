from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from entity.exceptions.bad_request_exception import BadRequestException
from entity.exceptions.internal_error_exception import InternalErrorException
import logging

logger = logging.getLogger(__name__)

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(Exception)
    async def general_exception_handler():
        return create_response("Internal Server Error", 500)

    @app.exception_handler(BadRequestException, RequestValidationError)
    async def bad_request_exception_handler(request, raw_exception: Exception):
        exception = BadRequestException(f"Bad Request", 400)
        return create_response(exception.detail, exception.status_code)

    @app.exception_handler(InternalErrorException)
    async def internal_error_exception_handler(request, exception: InternalErrorException):
        return create_response(exception.detail, exception.status_code)

def create_response(detail: str, status_code: int):
    return JSONResponse(
        status_code=status_code,
        content={"message": detail, "statusCode": status_code}
    )