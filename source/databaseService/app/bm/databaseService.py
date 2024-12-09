from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.databaseProvider import DatabaseProvider
from entities.httpStatusEnum import httpStatusCode
from entities.StockLogRequestModell import StockLogRequest
from database.databaseTableModells import Product, StockLog
from entities.DatabaseServiceResponseModel import DatabaseServiceResponse

class DatabaseService:
    def __init__(self):
        self.databaseProvider = DatabaseProvider()
        self.databaseProvider.initDb()

    def addItem(self, stockLogRequest: StockLogRequest) -> DatabaseServiceResponse:
        session = self.databaseProvider.getSession()
        databaseServiceResponse = DatabaseServiceResponse(httpStatusCode=None, statusMessage=None)
        try:
            # Check if stock log id is available
            stockLog = session.query(StockLog).filter_by(stockLogId=stockLogRequest.stockLogId).first()

            # Return conflict status if id is not available
            if stockLog:
                databaseServiceResponse.setHttpStatusCode(httpStatusCode.CONFLICT)
                databaseServiceResponse.setStatusMessage(f"Stock log with id {stockLog.stockLogId} already exists.")
                return databaseServiceResponse
 
            # Create new stock log entry
            newStockLog = StockLog(
                stockLogId=stockLogRequest.stockLogId,
                productId=stockLogRequest.productId,
                systemTimeIn=datetime.time(),
                systemTimeOut=None
            )
            session.add(newStockLog)
            session.commit()

            databaseServiceResponse.setHttpStatusCode(httpStatusCode.OK)
            databaseServiceResponse.setStatusMessage(f"Added stock log with id {stockLog.stockLogId}.")

            # Get product id, name and picture
            databaseServiceResponse = self.getProduct(stockLogRequest.productId, databaseServiceResponse)
            
            return databaseServiceResponse
        
        except Exception as e:
            session.rollback()
            databaseServiceResponse.setHttpStatusCode(httpStatusCode.SERVER_ERROR)
            databaseServiceResponse.setStatusMessage(e)
            return databaseServiceResponse
        
        finally:
            session.close()

    def removeItem(self, stockLogRequest: StockLogRequest) -> DatabaseServiceResponse:
        session = self.databaseProvider.getSession()
        databaseServiceResponse = DatabaseServiceResponse(httpStatusCode=None, statusMessage=None)
        try:
            # Check if stock log id exists
            stockLog = session.query(StockLog).filter_by(stockLogId=stockLogRequest.stockLogId).first()

            # Return bad request status if id does not exist
            if not stockLog:
                databaseServiceResponse.setHttpStatusCode(httpStatusCode.BAD_REQUEST)
                databaseServiceResponse.setStatusMessage(f"Stock log with id {stockLog.stockLogId} does not exist.")
                return databaseServiceResponse

            # Update system time out
            stockLog.systemTimeOut = datetime.time()
            session.commit()

            databaseServiceResponse.setHttpStatusCode(httpStatusCode.OK)
            databaseServiceResponse.setStatusMessage(f"Removed stock log with id {stockLog.stockLogId}.")
            
            # Get product id and name
            databaseServiceResponse = self.getProduct(stockLogRequest.productId, databaseServiceResponse)
            return databaseServiceResponse
        
        except Exception as e:
            session.rollback()
            databaseServiceResponse.setHttpStatusCode(httpStatusCode.SERVER_ERROR)
            databaseServiceResponse.setStatusMessage(e)
            return databaseServiceResponse

        finally:
            session.close()

    def addProducts(self, products: List[str]) -> httpStatusCode:
        session = self.databaseProvider.getSession()
        try:
            # Create product classes in database
            for product in products:
                productId = self.getNextId(session, True)
                newProduct = Product(
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
            nextId = session.query(func.max(getattr(Product.productId))).first()[0]
        else:
            nextId = session.query(func.max(getattr(StockLog.stockLogId))).first()[0]

        if nextId is None:
            nextId = 1
        else:
            nextId += 1
        return nextId
    
    def getProduct(self, session: Session, productId: int, databaseServiceResponse: DatabaseServiceResponse):
        product = session.query(Product).filter_by(productId=productId).first()
        if product:
            databaseServiceResponse.setProductId(product.productId)
            databaseServiceResponse.setProductName(product.productName)
            databaseServiceResponse.setProductPicture("This should be a picture")  # TODO: Replace with actual picture retrieval logic

        return databaseServiceResponse