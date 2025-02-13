from fastapi.responses import JSONResponse
import logging
from fastapi import Request

from bm.mail_preparing_service_ba import MailPreparingServiceBa
from entity.models.mail_data import MailUpdateData, MailErrorData
from entity.exceptions.internal_error_exception import InternalErrorException
from entity.enums.action import Action

class ApiBf:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.mail_preparing_service = MailPreparingServiceBa()

    async def prepare_mailing_data(self, mail_data_list: list[MailUpdateData], action: Action):
        try:
            self.mail_preparing_service.prepare_mail(mail_data_list, action)
            return JSONResponse(content={"message": "Successfully sent mail"}, status_code=200)
        
        except Exception as exception:
            self.logger.error(f"Exception: {exception}")
            raise InternalErrorException()
        
    async def prepare_mailing_data_error(self, data: MailErrorData):
        try:
            error_message = data["error_message"]
            self.mail_preparing_service.prepare_mail(error_message, Action.ERROR)
            return JSONResponse(content={"message": "Successfully sent error mail"}, status_code=200)
        
        except Exception as exception:
            self.logger.error(f"Exception: {exception}")
            raise InternalErrorException()
