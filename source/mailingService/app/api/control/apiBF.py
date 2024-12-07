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
            if action == Action.ADDED or action == Action.DELETED:
                mailData = MailData(validData["productId"], validData["productName"], validData["productPicture"], action)
            elif action == Action.ERROR:
                mailData = MailData(validData["productId"], validData["productName"], validData["productPicture"], action, validData["errorMessage"])
            mailSendingService = MailSendingService()
            mailSendingService.sendMail(mailData)
            return JSONResponse(content={"message": "Successfully send mail"}, status_code=200)
        except Exception as exception:
            self.logger.error(exception)
            raise InternalErrorException()

