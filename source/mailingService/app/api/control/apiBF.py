from bm.control.mailSendingService import MailSendingService
from bm.entity.Product import Product
import logging
from fastapi.responses import JSONResponse

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
        raise exception

async def prepareErrorMailingData(validData):
    try:
        errorMessage = validData["errorMessage"]
        mailSendingService = MailSendingService()
        mailSendingService.sendErrorMail(errorMessage)
        return JSONResponse(content={"message": "Successfully send mail"}, status_code=200)
    except Exception as exception:
        logger.error(exception)
        raise exception