from datetime import datetime
from typing import List
from fastapi import Request, JSONResponse
from entities.StockLogRequestModell import StockLogRequest
from databaseService import DatabaseService

class apiBF:
    def __init__(self, databaseService: DatabaseService):
        self.databaseService = databaseService

    def addItem(self, request:Request):
        # Create StockLogRequest object from request data
        stockLog = StockLogRequest(request["stockLogId"], request["productId"], request["timeIn"], request["timeout"])
        stockLogResponse = self.databaseService.addItem(stockLog)

        # Create response
        return JSONResponse(content = stockLogResponse.statusMessage, status_code = stockLogResponse.httpStatusCode)

    def removeItem(self, request:Request):
        # Create StockLogRequest object from request data
        stockLog = StockLogRequest(request["stockLogId"], request["productId"], request["timeIn"], request["timeout"])
        stockLogResponse = self.databaseService.removeItem(stockLog)

        # Create response
        return JSONResponse(content = stockLogResponse.statusMessage, status_code = stockLogResponse.httpStatusCode)
        
    def getNextID(self): 
        # Retrun next available ID
        return self.databaseService.getNextId(self.dataBaseService.databaseProvider.get_session(), False)