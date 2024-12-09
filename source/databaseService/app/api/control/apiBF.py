import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from bm.databaseService import DatabaseService
from entities.StockLogRequestModell import StockLogRequest
from entities.DatabaseServiceResponseModel import DatabaseServiceResponse
from entities.MailRequestModell import MailRequest
from entities.httpStatusEnum import httpStatusCode
from .mailingTrigger import triggerMailingService

class ApiBF:
    def __init__(self):
        self.databaseService = DatabaseService()
        self.logger = logging.getLogger(self.__class__.__name__)

    def addItem(self, request):
        # Create StockLogRequest object from request data
        stockLog = StockLogRequest(
            request["stockLogId"], 
            request["productId"]
            )
        
        # Add item to database
        databaseServiceResponse = self.databaseService.addItem(stockLog)

        # Create Mail request
        mailRequest = MailRequest(
            productId=databaseServiceResponse.getProductId(), 
            productName=databaseServiceResponse.getProductName(), 
            productPicture=databaseServiceResponse.getProductPicture(),
        )

        # Trigger error mail if failed to add item
        if databaseServiceResponse.getHttpStatusCode() != httpStatusCode.OK:
            logging.error(f"Error while adding new Item: {databaseServiceResponse.getStatusMessage()}")

            mailRequest.setErrorMessage(str(databaseServiceResponse.getStatusMessage()))
            response = triggerMailingService("sendErrorMail", mailRequest)
        
        # Trigger mail added event
        else:
            logging.info(f"Added new Item: {stockLog.stockLogId}")

            response = triggerMailingService("sendMailAdded", mailRequest)

        logging.info(f"Response from Mailing-Service: {response.get('message', 'No message available')}")

        # Create response
        return JSONResponse(content = str(databaseServiceResponse.getStatusMessage()), 
                            status_code = databaseServiceResponse.getHttpStatusCode().value)

    def removeItem(self, request):
        # Create StockLogRequest object from request data
        stockLog = StockLogRequest(
            request["stockLogId"], 
            request["productId"]
            )
        
        # Remove item from database
        databaseServiceResponse = self.databaseService.removeItem(stockLog)

        # Create Mail request
        mailRequest = MailRequest(
            productId=databaseServiceResponse.getProductId(), 
            productName=databaseServiceResponse.getProductName(), 
            productPicture=databaseServiceResponse.getProductPicture(),
        )

        # Trigger error mail if failed to remove item
        if databaseServiceResponse.getHttpStatusCode() != httpStatusCode.OK:
            logging.error(f"Error while removing Item: {databaseServiceResponse.getStatusMessage()}")

            mailRequest.setErrorMessage(str(databaseServiceResponse.getStatusMessage()))
            response = triggerMailingService("sendErrorMail", mailRequest)
        
        # Trigger mail removed event
        else:
            logging.info(f"Removed Item: {stockLog.stockLogId}")

            response = triggerMailingService("sendMailDeleted", mailRequest)

        logging.info(f"Response from Mailing-Service: {response.get('message', 'No message available')}")


        # Create response
        return JSONResponse(content = str(databaseServiceResponse.getStatusMessage()), 
                            status_code = databaseServiceResponse.getHttpStatusCode().value)
        
    def getNextID(self): 
        # Retrun next available ID
        return self.databaseService.getNextId(self.dataBaseService.databaseProvider.get_session(), False)
    
    def addProducts(self, products: list):
        # Add products to database
        self.databaseService.addProducts(products)
        logging.info(f"Added products: {products}")