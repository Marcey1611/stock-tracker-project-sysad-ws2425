import logging
from fastapi import HTTPException
from typing import Dict, Any


from bm.databaseService import DatabaseService
from entities.models import Request, Response, AppResponse
from .mailingTrigger import trigger_mailing_service

class ApiBf:
    database_service = DatabaseService()

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def handle_update_products_request(self, request: Request) -> Response:
        self.logger.info("Handling update products request.....................................................................................................")
        try:
            self.logger.info("1")
            mail_response = ApiBf.database_service.update_products(request)
            self.logger.info(mail_response)
            self.logger.info("2..................................................................................................................................")

            if mail_response:
                self.logger.info("3")
                trigger_mailing_service("send_update_mail", mail_response)
                self.logger.info("4")
            self.logger.info("5")
            return Response(status_code=200)

        except Exception as e:
            self.logger.error(f"Api-Bf: Error while updating products: {e}")
            trigger_mailing_service("send_error_mail", None)
            return Response(status_code = 500)

    def handle_app_request(self) -> AppResponse:
        self.logger.info("Update APP -------------------------------------------------------------------------------")
        try:
            return ApiBf.database_service.get_products()
        
        except Exception as e:
            self.logger.error(f"Api-Bf: Error while handling app-request: {e}")
            raise HTTPException(status_code=500, detail=f"Error while handling request: {e}")