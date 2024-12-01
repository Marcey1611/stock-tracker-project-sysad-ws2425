from fastapi.responses import JSONResponse
import logging

from bm.mailSendingServiceBA import MailSendingService
from entity.models.Product import Product
from entity.exceptions import InternalErrorException

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def prepareMailingData(validData):
    try:
        product = Product(validData["productId"], validData["productName"], validData["productPicture"])
        mailSendingService = MailSendingService()
        mailSendingService.sendMail(product)
        return JSONResponse(content={"message": "Successfully send mail"}, status_code=200)
    except Exception as exception:
        logger.error(exception)
        raise InternalErrorException()

async def prepareErrorMailingData(validData):
    try:
        errorMessage = validData["errorMessage"]
        mailSendingService = MailSendingService()
        mailSendingService.sendErrorMail(errorMessage)
        return JSONResponse(content={"message": "Successfully send mail"}, status_code=200)
    except Exception as exception:
        logger.error(exception)
        raise InternalErrorException()