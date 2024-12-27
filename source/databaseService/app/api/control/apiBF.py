import logging
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from bm.databaseService import DatabaseService

from entities.httpStatusEnum import httpStatusCode
from .mailingTrigger import triggerMailingService

class ApiBF:
    def __init__(self):
        self.databaseService = DatabaseService()
        self.logger = logging.getLogger(self.__class__.__name__)

    def addAmount(self, request):
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
        
    def resetAmounts(self): 
        try:
            return self.databaseService.resetAmounts().value
        
        except Exception as e:
            self.logger.error(f"An error occurred while reseting products amount: {e}")
            return JSONResponse(content = "An unexpected error occurred", status_code = httpStatusCode.SERVER_ERROR.value)

    
    def addProducts(self, products: list):
        try:
            # Add products to database
            self.databaseService.addProducts(products)
            logging.info(f"Added products: {products}")

            return JSONResponse(content = "Created products", status_code = httpStatusCode.OK.value)

        except Exception as e:
            self.logger.error(f"An error occurred while adding products: {e}")
            return JSONResponse(content = "An unexpected error occurred", status_code = httpStatusCode.SERVER_ERROR.value)