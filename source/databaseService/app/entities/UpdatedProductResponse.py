from typing import Optional

class UpdatedProductResponse:
    def __init__(self, productId: int, productName:str, productPicture: str, productAmountTotal: int, productAmountAdded: int, errorMessage: Optional[str] = None):
        self.productId = productId
        self.productName = productName
        self.productPicture = productPicture
        self.productAmountTotal = productAmountTotal
        self.productAmountAdded = productAmountAdded
        self.errorMessage = errorMessage

    def getProductId(self) -> int:
        return self.productId
    
    def getProductName(self) -> str:
        return self.productName
    
    def getProductPicture(self) -> str:
        # TODO: Add product picture handling
        return ""
    
    def getproductAmountTotal(self) -> int:
        return self.productAmountTotal
    
    def getproductAmountAdded(self) -> int:
        return self.productAmountAdded
    
    def getErrorMessage(self) -> Optional[str]:
        return self.errorMessage
    
    def setProductId(self, productId: int):
        self.productId = productId

    def setProductName(self, productName: str):
        self.productName = productName

    def setProductPicture(self, productPicture: str):
        self.productPicture = productPicture

    def setproductAmountTotal(self, productAmountTotal: int):
        self.productAmountTotal = productAmountTotal

    def setproductAmountAdded(self, productAmountAdded: int):
        self.productAmountAdded = productAmountAdded

    def setErrorMessage(self, errorMessage: Optional[str]):
        self.errorMessage = errorMessage

    def toDict(self) -> dict:
        return {
            "productId": self.productId,
            "productName": self.productName,
            "productPicture": self.productPicture,
            "productAmount": self.productAmount,
            "errorMessage": self.errorMessage,
        }