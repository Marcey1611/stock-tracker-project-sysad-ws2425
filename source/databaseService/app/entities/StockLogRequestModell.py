from datetime import datetime

class StockLogRequest:
    def __init__(self, stockLogId: int, productId: int, timeIn: datetime, timeOut: datetime):
        self.stockLogId = stockLogId
        self.productId = productId
        self.timeIn = self.parse_time(timeIn)
        self.timeOut = self.parse_time(timeOut)

    def getStockLogId(self) -> int:
        return self.stockLogId
    
    def getProductId(self) -> int:
        return self.productId
    
    def getTimeIn(self) -> datetime:
        return self.timeIn
    
    def getTimeOut(self) -> datetime:
        return self.timeOut

    def setStockLogId(self, stockLogId: int):
        self.stockLogId = stockLogId

    def setProductId(self, productId: int):
        self.productId = productId

    def setTimeIn(self, timeIn: datetime):
        self.timeIn = self.parse_time(timeIn)

    def setTimeOut(self, timeOut: datetime):
        self.timeOut = self.parse_time(timeOut)

    