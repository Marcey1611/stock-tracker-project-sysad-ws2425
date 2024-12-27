from entity.enums import Action

class MailData:
    def __init__(self, productId: int, productName: str, productAmountAdded: int, productAmountTotal: int, action: Action):
        self.__productId = productId
        self.__productName = productName
        self.__productAmountAdded = productAmountAdded
        self.__productAmountTotal = productAmountTotal
        self.__action = action


    def getProductId(self) -> int:
        return self.__productId
    
    def getProductName(self) -> str:
        return self.__productName
    
    def getAction(self) -> Action:
        return self.__action
    
    def getProductAmountAdded(self) -> int:
        return self.__productAmountAdded
    
    def getProductAmountTotal(self) -> int:
        return self.__productAmountTotal