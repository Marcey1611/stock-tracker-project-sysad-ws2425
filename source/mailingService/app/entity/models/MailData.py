from entity.enums import Action

class MailData:
    def __init__(self, productId: int, productName: str, productPicture: str, productAmountChanged: int, productAmountTotal: int, action: Action):
        self.__productId = productId
        self.__productName = productName
        self.__productPicture = productPicture
        self.__productAmountChanged = productAmountChanged
        self.__productAmountTotal = productAmountTotal
        self.__action = action


    def getProductId(self) -> int:
        return self.__productId
    
    def getProductName(self) -> str:
        return self.__productName
    
    def getProductPicture(self) -> str:
        return self.__productPicture
    
    def getAction(self) -> Action:
        return self.__action
    
    def getProductAmountChanged(self) -> int:
        return self.__productAmountChanged
    
    def getProductAmountTotal(self) -> int:
        return self.__productAmountTotal