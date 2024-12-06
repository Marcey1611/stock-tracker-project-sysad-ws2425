class StockLogResponse:
    def __init__(self, httpStatusCode: int, statusMessage: str):
        self.httpStatusCode = httpStatusCode
        self.httpStatusCode = statusMessage

    def getHttpStatusCode(self) -> int:
        return self.httpStatusCode
    
    def getStatusMessage(self) -> str:
        return self.statusMessage
    
    def setHttpStatusCode(self, httpStatusCode: int):
        self.httpStatusCode = httpStatusCode

    def setStatusMessage(self, statusMessage: str):
        self.statusMessage = statusMessage