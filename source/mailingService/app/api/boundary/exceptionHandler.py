from fastapi import FastAPI
from fastapi.responses import JSONResponse

from entity.exceptions import BadRequestException, InternalErrorException

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(Exception)
    async def mailSendingExceptionHandler():
        return response("Unexpected Exception!", 500)

    @app.exception_handler(BadRequestException)
    async def badRequestExceptionHandler(request, exception: BadRequestException):
        return response(exception.detail, exception.status_code)

    @app.exception_handler(InternalErrorException)
    async def badRequestExceptionHandler(request, exception: InternalErrorException):
        return response(exception.detail, exception.status_code)

def response(detail: str, statusCode: int):
    return JSONResponse(
            status_code=statusCode,
            content={"message": detail, "statusCode": statusCode}
        )