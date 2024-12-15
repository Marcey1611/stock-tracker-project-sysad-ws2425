from fastapi.responses import JSONResponse
import logging

from bm.mailSendingServiceBA import MailSendingService
from entity.models.MailData import MailData
from entity.exceptions import InternalErrorException
from entity.enums import Action

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

class ApiBF:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    async def prepareMailingData(self, validData, action: Action):
        try:
            mailDataArray = []
            self.logger.info("Prepare mail data for action: " + str(action))
            for product in validData:
                mailData = MailData(product["productId"], product["productName"], product["productPicture"], product["productAmountAdded"], product["productAmountTotal"], action)
                self.logger.info(mailData)
                mailDataArray.append(mailData)
            mailSendingService = MailSendingService()
            mailSendingService.sendMail(mailDataArray[0])
            return JSONResponse(content={"message": "Successfully send mail"}, status_code=200)
        except Exception as exception:
            self.logger.error(exception)
            raise InternalErrorException()

