class MailError:
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage

    def getErrorMessage(self):
        return self.errorMessage
    
    def setErrorMessage(self, errorMessage):
        self.errorMessage = errorMessage