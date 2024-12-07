import logging
from datetime import datetime
from typing import List
from fastapi import Request, JSONResponse
from app.bm.databaseService import DatabaseService
from entities.StockLogRequestModell import StockLogRequest
from app.entities.DatabaseServiceResponseModel import DatabaseServiceResponse
from app.entities.MailRequestModell import MailRequest
from mailingTrigger import triggerMailingService

class ApiBF:
    def __init__(self):
        self.databaseService = DatabaseService()

    def addItem(self, request:Request):
        # Create StockLogRequest object from request data
        stockLog = StockLogRequest(
            request["stockLogId"], 
            request["productId"], 
            request["timeIn"], 
            request["timeout"]
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
        if databaseServiceResponse.getHttpStatusCode() != 200:
            logging.error(f"Error while adding new Item: {databaseServiceResponse.getStatusMessage()}")

            mailRequest.setErrorMessage(databaseServiceResponse.getStatusMessage())
            response = triggerMailingService("sendErrorMail", mailRequest)
        
        # Trigger mail added event
        else:
            logging.info(f"Added new Item: {stockLog.stockLogId}")

            response = triggerMailingService("sendMailAdded", mailRequest)

        logging.info(f"Response from Mailing-Service: {response.get('message', 'No message available')}")

        # Create response
        return JSONResponse(content = databaseServiceResponse.getStatusMessage, status_code = databaseServiceResponse.getHttpStatusCode)

    def removeItem(self, request:Request):
        # Create StockLogRequest object from request data
        stockLog = StockLogRequest(
            request["stockLogId"], 
            request["productId"], 
            request["timeIn"], 
            request["timeout"]
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
        if databaseServiceResponse.getHttpStatusCode() != 200:
            logging.error(f"Error while removing Item: {databaseServiceResponse.getStatusMessage()}")

            mailRequest.setErrorMessage(databaseServiceResponse.getStatusMessage())
            response = triggerMailingService("sendErrorMail", mailRequest)
        
        # Trigger mail removed event
        else:
            logging.info(f"Removed Item: {stockLog.stockLogId}")

            response = triggerMailingService("sendMailDeleted", mailRequest)

        logging.info(f"Response from Mailing-Service: {response.get('message', 'No message available')}")


        # Create response
        return JSONResponse(content = databaseServiceResponse.getStatusMessage(), status_code = databaseServiceResponse.getHttpStatusCode())
        
    def getNextID(self): 
        # Retrun next available ID
        return self.databaseService.getNextId(self.dataBaseService.databaseProvider.get_session(), False)