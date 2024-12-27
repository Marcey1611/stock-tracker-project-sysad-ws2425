from fastapi.responses import JSONResponse
import logging
from fastapi import Request

from bm.mailSendingServiceBA import MailSendingService
from entity.models.MailData import MailData
from entity.exceptions import InternalErrorException
from entity.enums import Action

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

class ApiBF:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    async def prepareMailingData(self, validData: Request, action: Action):
        try:
            mailDataList = []
            for product in validData:
                mailData = MailData(product["productId"], product["productName"], product["productAmountAdded"], product["productAmountTotal"], action)
                mailDataList.append(mailData)
            mailSendingService = MailSendingService()
            mailSendingService.sendMail(mailDataList, action) 
            return JSONResponse(content={"message": "Successfully send mail"}, status_code=200)
        
        except Exception as exception:
            self.logger.error(f"Exception: {exception}")
            raise InternalErrorException()
        
    async def prepareMailingDataError(self, validData: Request):
        try:
            errorMessage = validData["errorMessage"]
            mailSendingService = MailSendingService()
            mailSendingService.sendMail(errorMessage, Action.ERROR)
            return JSONResponse(content={"message": "Successfully send error mail"}, status_code=200)
        
        except Exception as exception:
            self.logger.error(f"Exception: {exception}")
            raise InternalErrorException()

