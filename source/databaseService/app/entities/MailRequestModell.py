from typing import Optional

class MailRequest:
    def __init__(self, productId: int, productName:str, productPicture: str, errorMessage: Optional[str] = None):
        self.productId = productId
        self.productName = productName
        self.productPicture = productPicture
        self.errorMessage = errorMessage

    def getProductId(self) -> int:
        return self.productId
    
    def getProductName(self) -> str:
        return self.productName
    
    def getProductPicture(self) -> str:
        return self.productPicture
    
    def getErrorMessage(self) -> Optional[str]:
        return self.errorMessage
    
    def setProductId(self, productId: int):
        self.productId = productId

    def setProductName(self, productName: str):
        self.productName = productName

    def setProductPicture(self, productPicture: str):
        self.productPicture = productPicture

    def setErrorMessage(self, errorMessage: Optional[str]):
        self.errorMessage = errorMessage

    def toDict(self) -> dict:
        return {
            "productId": self.productId,
            "productName": self.productName,
            "productPicture": self.productPicture,
            "errorMessage": self.errorMessage,
        }