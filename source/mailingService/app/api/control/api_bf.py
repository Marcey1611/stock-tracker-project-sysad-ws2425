from fastapi.responses import JSONResponse
import logging
from fastapi import Request

from bm.mail_preparing_service_ba import MailPreparingServiceBa
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
                    product["product_id"], 
                    product["product_name"], 
                    product["product_amount_changed"], 
                    product["product_amount_total"], 
                    action
                )
                mail_data_list.append(mail_data)
            mail_preparing_service = MailPreparingServiceBa()
            mail_preparing_service.prepare_mail(mail_data_list, action)
            return JSONResponse(content={"message": "Successfully sent mail"}, status_code=200)
        
        except Exception as exception:
            self.logger.error(f"Exception: {exception}")
            raise InternalErrorException()
        
    async def prepare_mailing_data_error(self, valid_data: Request):
        try:
            error_message = valid_data["error_message"]
            mail_preparing_service = MailPreparingServiceBa()
            mail_preparing_service.prepare_mail(error_message, Action.ERROR)
            return JSONResponse(content={"message": "Successfully sent error mail"}, status_code=200)
        
        except Exception as exception:
            self.logger.error(f"Exception: {exception}")
            raise InternalErrorException()
