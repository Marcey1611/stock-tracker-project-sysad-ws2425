from datetime import datetime

class StockLogRequest:
    def __init__(self, stockLogId: int, productId: int, timeIn: str, timeOut: str):
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

    def setTimeIn(self, timeIn: str):
        self.timeIn = self.parse_time(timeIn)

    def setTimeOut(self, timeOut: str):
        self.timeOut = self.parse_time(timeOut)

    