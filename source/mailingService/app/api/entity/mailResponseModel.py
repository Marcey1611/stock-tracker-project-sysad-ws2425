from .mailResponseStatusEnum import Status
from typing import Union

class MailResponse:
    def __init__(self, status: Status, message):
        self.message = message
        self.status = status

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message
    
    def setStatus(self, status):
        self.status = status
    
    def setMessage(self, message):
        self.message = message