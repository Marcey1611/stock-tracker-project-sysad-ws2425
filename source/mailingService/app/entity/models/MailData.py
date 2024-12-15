from entity.enums import Action

class MailData:
    def __init__(self, productId: int, productName: str, productPicture: str, action: Action, errorMessage: str = None):
        self.productId = productId
        self.productName = productName
        self.productPicture = productPicture
        self.action = action
        self.errorMessage = errorMessage