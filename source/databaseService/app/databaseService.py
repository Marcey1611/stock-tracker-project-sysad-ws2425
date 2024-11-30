from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from httpStatusEnum import httpStatus
from StockLogRequestModell import StockLogRequest
from databaseProvider import DatabaseProvider

class DatabaseService:
    def __init__(self, dbProvider):
        self.dbProvider = dbProvider

    def addItem(self, stockLog: StockLogRequest):
        session = self.db_provider.get_session()
        try:
            # Check if stock log id is available
            stockLog = session.query(self.dbProvider.Base.stockLog).filter_by(stockLogId=stockLog.stockLogId).first()

            # Return conflict status if id is not available
            if stockLog:
                return httpStatus.CONFLICT, f"Stock log with id {stockLog.stockLogId} already exists."

            # Create new stock log entry
            newStockLog = self.dbProvider.Base.stockLog(
                product_id=stockLog.productId,
                system_time_in=stockLog.timeIn.time(),
                system_time_out=stockLog.timeOut.time()
            )
            session.add(newStockLog)
            session.commit()

            return httpStatus.OK
        except Exception as e:
            session.rollback()
            return httpStatus.SERVER_ERROR, str(e)
        finally:
            session.close()

    def removeItem(self, stockLog: StockLogRequest):
        session = self.db_provider.get_session()
        try:
            stockLog = session.query(self.dbProvider.Base.stockLog).filter_by(stockLogId=stockLog.stockLogId).first()

            # Return bad request status if id does not exist
            if not stockLog:
                return httpStatus.BAD_REQUEST, f"Stock log with id {stockLog.stockLogId} does not exist."

            # Update system time out
            stockLog.systemTimeOut = datetime.time()
            session.commit()

            return httpStatus.OK
        except Exception as e:
            session.rollback()
            return httpStatus.SERVER_ERROR, str(e)
        finally:
            session.close()

    def addProducts(self, databaseProvider: DatabaseProvider, products: List[str]):
        session = databaseProvider.get_session()
        try:
            for product in products:
                productId = self.getNextId(session, 'product')
                new_product = self.dbProvider.Base.product(
                    productId=productId, 
                    productName=product
                    )
                session.add(new_product)

            session.commit()
            return f"Product-classes have been created successfully."
        except Exception as e:
            session.rollback()
            return httpStatus.SERVER_ERROR, str(e)
        finally:
            session.close()

    def getNextId(self, session: Session, tableName: str) -> int:
        if tableName == 'product':
            nextId = session.query(func.max(getattr(self.dbProvider.Base.products.productId))).first()[0]
        else:
            nextId = session.query(func.max(getattr(self.dbProvider.Base.stockLog.stockLogId))).first()[0]

        if nextId is None:
            nextId = 1
        else:
            nextId += 1
        return nextId