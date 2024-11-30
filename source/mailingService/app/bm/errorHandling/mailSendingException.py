from fastapi import HTTPException
from fastapi.responses import JSONResponse

class MailSendingException(HTTPException):
    def __init__(self):
        self.status_code = 500
        self.detail = "Error: Something went wrong while sending the email."
        #super().__init__(status_code=self.statusCode, detail="opmfepomep")

    def response(self):
        return JSONResponse(
            status_code=self.status_code,
            content={"message": self.detail}
        )