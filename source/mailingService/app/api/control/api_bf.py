from fastapi.responses import JSONResponse
import logging
from fastapi import Request

from bm.mail_sending_service_ba import MailSendingServiceBa
from entity.models.mail_data import MailData
from entity.exceptions.internal_error_exception import InternalErrorException
from entity.enums.action import Action

class ApiBf:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    async def prepare_mailing_data(self, valid_data: Request, action: Action):
        try:
            mail_data_list = []
            for product in valid_data:
                mail_data = MailData(
                    product["productId"], 
                    product["productName"], 
                    product["productAmountAdded"], 
                    product["productAmountTotal"], 
                    action
                )
                mail_data_list.append(mail_data)
            mail_sending_service = MailSendingServiceBa()
            mail_sending_service.send_mail(mail_data_list, action)
            return JSONResponse(content={"message": "Successfully sent mail"}, status_code=200)
        
        except Exception as exception:
            self.logger.error(f"Exception: {exception}")
            raise InternalErrorException()
        
    async def prepare_mailing_data_error(self, valid_data: Request):
        try:
            error_message = valid_data["errorMessage"]
            mail_sending_service = MailSendingServiceBa()
            mail_sending_service.send_mail(error_message, Action.ERROR)
            return JSONResponse(content={"message": "Successfully sent error mail"}, status_code=200)
        
        except Exception as exception:
            self.logger.error(f"Exception: {exception}")
            raise InternalErrorException()
