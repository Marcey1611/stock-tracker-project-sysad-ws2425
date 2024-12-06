from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from entities.httpStatusEnum import httpStatusCode
from entities.StockLogRequestModell import StockLogRequest
from entities.StockLogResponseModell import StockLogResponse
from database.databaseProvider import DatabaseProvider

class DatabaseService:
    def __init__(self, databaseProvider: DatabaseProvider):
        self.databaseProvider = databaseProvider

    def addItem(self, stockLog: StockLogRequest) -> StockLogResponse:
        session = self.databaseProvider.get_session()
        stockLogResponse = StockLogResponse(httpStatusCode=None, statusMessage=None)
        try:
            # Check if stock log id is available
            stockLog = session.query(self.dbProvider.Base.stockLog).filter_by(stockLogId=stockLog.stockLogId).first()

            # Return conflict status if id is not available
            if stockLog:
                stockLogResponse.setHttpStatusCode(httpStatusCode.CONFLICT)
                stockLogResponse.setStatusMessage(f"Stock log with id {stockLog.stockLogId} already exists.")
                return stockLogResponse
 
            # Create new stock log entry
            newStockLog = self.dbProvider.Base.stockLog(
                product_id=stockLog.productId,
                system_time_in=stockLog.timeIn.time(),
                system_time_out=stockLog.timeOut.time()
            )
            session.add(newStockLog)
            session.commit()

            stockLogResponse.setHttpStatusCode(httpStatusCode.OK)
            stockLogResponse.setStatusMessage(f"Added stock log with id {stockLog.stockLogId}.")
            return stockLogResponse
        
        except Exception as e:
            session.rollback()
            stockLogResponse.setHttpStatusCode(httpStatusCode.SERVER_ERROR)
            stockLogResponse.setStatusMessage(e)
            return stockLogResponse
        
        finally:
            session.close()

    def removeItem(self, stockLog: StockLogRequest) -> StockLogResponse:
        session = self.databaseProvider.get_session()
        stockLogResponse = StockLogResponse(httpStatusCode=None, statusMessage=None)
        try:
            # Check if stock log id exists
            stockLog = session.query(self.dbProvider.Base.stockLog).filter_by(stockLogId=stockLog.stockLogId).first()

            # Return bad request status if id does not exist
            if not stockLog:
                stockLogResponse.setHttpStatusCode(httpStatusCode.BAD_REQUEST)
                stockLogResponse.setStatusMessage(f"Stock log with id {stockLog.stockLogId} does not exist.")
                return stockLogResponse

            # Update system time out
            stockLog.systemTimeOut = datetime.time()
            session.commit()

            stockLogResponse.setHttpStatusCode(httpStatusCode.OK)
            stockLogResponse.setStatusMessage(f"Removed stock log with id {stockLog.stockLogId}.")
            return stockLogResponse
        
        except Exception as e:
            session.rollback()
            stockLogResponse.setHttpStatusCode(httpStatusCode.SERVER_ERROR)
            stockLogResponse.setStatusMessage(e)
            return stockLogResponse

        finally:
            session.close()

    def addProducts(self, products: List[str]) -> httpStatusCode:
        session = self.databaseProvider.get_session()
        try:
            # Create product classes in database
            for product in products:
                productId = self.getNextId(session, True)
                newProduct = self.dbProvider.Base.product(
                    productId=productId, 
                    productName=product
                    )
                session.add(newProduct)

            session.commit()
            return httpStatusCode.OK
        
        except Exception as e:
            session.rollback()
            return httpStatusCode.SERVER_ERROR
        
        finally:
            session.close()

    def getNextId(self, session: Session, addProducts: bool) -> int:
        if addProducts:
            nextId = session.query(func.max(getattr(self.dbProvider.Base.products.productId))).first()[0]
        else:
            nextId = session.query(func.max(getattr(self.dbProvider.Base.stockLog.stockLogId))).first()[0]

        if nextId is None:
            nextId = 1
        else:
            nextId += 1
        return nextId