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

    def handle_init_products_request(self, request: Request) -> Response:
        try:
            ApiBf.database_service.intitalize_products(request)
            return Response(status_code=200)

        except Exception as e:
            self.logger.error(f"Api-Bf: Error while initializing products: {e}")
            return Response(status_code = 500)

    def handle_update_request(self, request: Request, is_add: bool) -> Response:
        try: 
            updated_products_dict = ApiBf.database_service.update_products_amount(request, is_add)
            # trigger_mailing_service("sendMailAdded" if is_add else "sendMailDeleted", updated_products_dict)
            return Response(status_code = 200)
        
        except HTTPException as http_exception:
            self.logger.error(f"Api-Bf: Error while updating products amount: {http_exception}")
            return Response(status_code = http_exception.status_code)

        except Exception as e:
            self.logger.error(f"Api-Bf: Error while updating products amount: {e}")
            return Response(status_code = 500)
      
    def handle_reset_request(self) -> Response: 
        try:
            ApiBf.database_service.reset_amounts()
            return Response(status_code = 200)
        
        except Exception as e:
            self.logger.error(f"Api-Bf: Error while reseting products amount: {e}")
            return Response(status_code = 500)

    def handle_app_request(self) -> AppResponse:
        try:
            return ApiBf.database_service.get_products()
        
        except Exception as e:
            self.logger.error(f"Api-Bf: Error while handling app-request: {e}")
            raise HTTPException(status_code=500, detail=f"Error while handling request: {e}")