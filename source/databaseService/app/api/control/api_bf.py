import logging
from fastapi import HTTPException

from bm.database_service import DatabaseService
from entities.models import Request, Response, AppResponse
from .mailing_trigger import trigger_mailing_service

class ApiBf:
    def __init__(self):
        self.database_service = DatabaseService()
        self.logger = logging.getLogger(self.__class__.__name__)

    def handle_update_products_request(self, request: Request) -> Response:
        try:
            mail_response = ApiBf.self.database_service.update_products(request)

            if mail_response:
                trigger_mailing_service("send_update_mail", mail_response)
                
            return Response(status_code=200)

        except Exception as e:
            self.logger.error(f"Api-Bf: Error while handling update-request: {e}")
            trigger_mailing_service("send_error_mail", None)
            return Response(status_code = 500)

    def handle_app_request(self) -> AppResponse:
        try:
            return ApiBf.self.database_service.get_products()
        
        except Exception as e:
            self.logger.error(f"Api-Bf: Error while handling app-request: {e}")
            raise HTTPException(status_code=500, detail=f"Error while handling app-request: {e}")