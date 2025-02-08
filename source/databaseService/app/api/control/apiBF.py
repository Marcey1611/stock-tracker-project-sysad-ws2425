import logging
from fastapi import HTTPException
from typing import Dict, Any


from bm.databaseService import DatabaseService
from entities.models import Request, Response, AppResponse
from .mailingTrigger import trigger_mailing_service

class ApiBF:
    database_service = DatabaseService()

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def handle_update_request(self, request: Request, is_add: bool) -> Response:
        try: 
            updated_products_dict = ApiBF.database_service.update_products_amount(is_add, request)
            # trigger_mailing_service("sendMailAdded" if is_add else "sendMailDeleted", updated_products_dict)
            return Response(status_code = 200)
        
        except HTTPException as http_exception:
            return Response(status_code = http_exception.status_code)

        except Exception as e:
            self.logger.error(f"Error while updating products amount: {e}")
            return Response(status_code = 500)
      
    def handle_reset_request(self) -> Response: 
        try:
            ApiBF.database_service.reset_amounts()

            return Response(status_code = 200)
        
        except Exception as e:
            self.logger.error(f"Error while reseting products amount: {e}")
            return Response(status_code = 500)

    def handle_app_request(self) -> Dict[Any, dict]:
        try:
            all_products_dict = ApiBF.database_service.get_products()
            return {key: value.dict() for key, value in all_products_dict.items()}
        
        except Exception as e:
            self.logger.error(f"Error while handling app-request: {e}")
            raise HTTPException(status_code=500, detail="Error while handling request")

    def handle_create_request(self, products: list):
        try:
            ApiBF.database_service.add_products(products)
            logging.info(f"Added products: {products}")

        except Exception as e:
            self.logger.error(f"Error while adding products: {e}")