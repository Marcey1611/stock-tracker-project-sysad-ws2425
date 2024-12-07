from typing import Optional

class DatabaseServiceResponse:
    def __init__(self, httpStatusCode: int, statusMessage: str, productId: Optional[int] = None, productName: Optional[str] = None, productPicture: Optional[str] = None):
        self.httpStatusCode = httpStatusCode
        self.statusMessage = statusMessage
        self.productId = productId
        self.productName = productName
        self.productPicture = productPicture

    def getHttpStatusCode(self) -> int:
        return self.httpStatusCode
    def getStatusMessage(self) -> str:
        return self.statusMessage

    def getProductId(self) -> Optional[int]:
        return self.productId

    def getProductName(self) -> Optional[str]:
        return self.productName

    def getProductPicture(self) -> Optional[str]:
        return self.productPicture

    def setHttpStatusCode(self, httpStatusCode: int):
        self.httpStatusCode = httpStatusCode

    def setStatusMessage(self, statusMessage: str):
        self.statusMessage = statusMessage
    
    def setProductId(self, productId: int):
        self.productId = productId
    
    def setProductName(self, productName: str):
        self.productName = productName
    
    def setProductPicture(self, productPicture: str):
        self.productPicture = productPicture