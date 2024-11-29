class Mail:
    def __init__(self, productId, productName):
        self.productId = productId
        self.productName = productName

    def getProductId(self):
        return self.productId
    
    def getProductName(self):
        return self.productName
    
    def setProductId(self, productId):
        self.productId = productId

    def setProductName(self, productName):
        self.productName = productName