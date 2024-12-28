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
            # Update product amount in database
            updatedProductIds = request.get("productId")
            databaseServiceResponseList = self.databaseService.updateProductsAmount(True, updatedProductIds)
            triggerMailingService("sendMailAdded", databaseServiceResponseList)

            # Try againg if failed to trigger mailing-service
            #for _ in range(2):
            #    # Trigger mail added event
            #    response = triggerMailingService("sendMailAdded", databaseServiceResponseList)

            #    if response.get('status_code') == httpStatusCode.OK:
            #        break

            # Create response
            return JSONResponse(content = "Updatet products", status_code = httpStatusCode.OK.value)

        except HTTPException as http_exception:
            self.logger.error(f"HTTP Exception: {http_exception.detail}")
            return JSONResponse(content = "An HTTP Exception occured", status_code = http_exception.status_code.value)

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            return JSONResponse(content = "An unexpected error occurred", status_code = httpStatusCode.SERVER_ERROR.value)

    def removeAmount(self, request):
        try:
            # Update product amount in database
            updatedProductIds = request.get("productId")
            databaseServiceResponseList = self.databaseService.updateProductsAmount(False, updatedProductIds)
            self.logger.info("BEFORE")
            triggerMailingService("sendMailDeleted", databaseServiceResponseList)
            self.logger.info("AFTER")

            # Try againg if failed to trigger mailing-service
            #for _ in 2:
            #    # Trigger mail added event
            #    response = triggerMailingService("sendMailDeleted", databaseServiceResponseList)

            #    if response.get('status_code') == httpStatusCode.OK:
            #        break

            # Create response
            return JSONResponse(content = "Updatet products", status_code = httpStatusCode.OK.value)

        except HTTPException as http_exception:
            self.logger.error(f"HTTP Exception: {http_exception.detail}")
            return JSONResponse(content = "An HTTP Exception occured", status_code = http_exception.status_code.value)

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            return JSONResponse(content = "An unexpected error occurred", status_code = httpStatusCode.SERVER_ERROR.value)
        
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