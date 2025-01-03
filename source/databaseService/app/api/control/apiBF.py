import logging
from fastapi import HTTPException

from bm.databaseService import DatabaseService
from entities.models import Request, Response
from .mailingTrigger import triggerMailingService

class ApiBF:
    databaseService = DatabaseService()

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def handleUpdateRequest(self, request: Request, isAdd: bool) -> Response:
        try: 
            updatedProductsDict = ApiBF.databaseService.updateProductsAmount(isAdd,request.ids)
            triggerMailingService("sendMailAdded" if isAdd else "sendMailDeleted", updatedProductsDict)
            return Response(statusCode = 200)
        
        except HTTPException as http_exception:
            return Response(statusCode = http_exception.status_code)

        except Exception as e:
            self.logger.error(f"Error while updating products amount: {e}")
            return Response(statusCode = 500)
      
    def handleResetRequest(self) -> Response: 
        try:
            return Response(statusCode=200)
        
        except Exception as e:
            self.logger.error(f"Error while reseting products amount: {e}")
            return Response(statusCode = 500)

    def handleCreateRequest(self, products: list):
        try:
            ApiBF.databaseService.addProducts(products)
            logging.info(f"Added products: {products}")

        except Exception as e:
            self.logger.error(f"Error while adding products: {e}")