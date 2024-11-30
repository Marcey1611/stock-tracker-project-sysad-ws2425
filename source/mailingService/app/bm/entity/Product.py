class Product:
    def __init__(self, productId, productName, productPicture):
        self.productId = productId
        self.productName = productName
        self.productPicture = productPicture

    def getProductId(self):
        return self.productId
    
    def getProductName(self):
        return self.productName
    
    def getProductPicture(self):
        return self.productPicture
    
    def setProductId(self, productId):
        self.productId = productId

    def setProductName(self, productName):
        self.productName = productName

    def setProductPicture(self, productPicture):
        self.productPicture = productPicture