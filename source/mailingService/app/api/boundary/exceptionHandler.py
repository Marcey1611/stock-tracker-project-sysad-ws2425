from fastapi import FastAPI
from fastapi.responses import JSONResponse

from entity.exceptions.BadRequestException import BadRequestException
from entity.exceptions.InternalErrorException import InternalErrorException
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def registerExceptionHandlers(app: FastAPI):

    @app.exceptionHandler(Exception)
    async def mailSendingExceptionHandler():
        return response("Internal Server Error", 500)

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