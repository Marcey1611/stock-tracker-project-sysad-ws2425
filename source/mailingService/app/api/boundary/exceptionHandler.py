from fastapi import Request
from bm.errorHandling.mailSendingException import MailSendingException
from main import app

@app.exception_handler(MailSendingException)
async def mailSendingExceptionHandler(request: Request, exception: MailSendingException):
    return {"exception.response()": "pmdpovmer"}