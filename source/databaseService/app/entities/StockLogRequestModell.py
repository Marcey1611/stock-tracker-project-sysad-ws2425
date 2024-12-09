from datetime import datetime
from typing import Optional

class StockLogRequest:
    def __init__(self, stockLogId: int, productId: int):
        self.stockLogId = stockLogId
        self.productId = productId

    def getStockLogId(self) -> int:
        return self.stockLogId
    
    def getProductId(self) -> int:
        return self.productId

    def setStockLogId(self, stockLogId: int):
        self.stockLogId = stockLogId

    def setProductId(self, productId: int):
        self.productId = productId