from source.mailingService.app.entity.enums.Action import Action

class MailData:
    def __init__(self, productId: int, productName: str, productAmountChanged: int, productAmountTotal: int, action: Action):
        self.__productId = productId
        self.__productName = productName
        self.__productAmountChanged = productAmountChanged
        self.__productAmountTotal = productAmountTotal
        self.__action = action


    def getProductId(self) -> int:
        return self.__productId
    
    def getProductName(self) -> str:
        return self.__productName
    
    def getAction(self) -> Action:
        return self.__action
    
    def getProductAmountChanged(self) -> int:
        return self.__productAmountChanged
    
    def getProductAmountTotal(self) -> int:
        return self.__productAmountTotal