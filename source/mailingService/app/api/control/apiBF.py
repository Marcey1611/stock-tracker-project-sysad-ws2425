from businessModule.control.mailSendingService import MailSendingService
from api.entity.mailModel import Mail
from api.entity.mailErrorModel import MailError
from api.entity.mailResponseModel import MailResponse
from api.entity.mailResponseStatusEnum import Status
import json

async def prepareMailingData(sentData):
    try:
        data = await sentData.json()
        mailModel = Mail(data["productId"], data["productName"])
        mailSendingService = MailSendingService(mailModel["productName"], mailModel["productId"], None)
        mailSendingService.sendMail
        mailResponseSuccess = MailResponse(Status.SUCCESS, "Successfully send mail")
        return mailResponseSuccess.__dict__ #later this would be a method call
    except Exception as exception:
        mailResponseError = MailResponse(Status.ERROR, exception) #something like this should the called method return
        #return mailResponseError.__dict__ #later this would be a method call
        return {"response": "error apiBF send Mail"}

async def prepareErrorMailingData(sentData):
    try:
        data = await sentData.json()
        mailErrorModel = MailError(data["errorMessage"])
                
        #TODO Call method to send mail as return value.
        mailErrorResponse = MailResponse(Status.SUCCESS, "Successfull send error mail") #something like this should the called method return
        return mailErrorResponse.__dict__ #later this would be a method call
    except Exception as exception:
        mailErrorResponseError = MailResponse(Status.ERROR, exception) #something like this should the called method return
        return mailErrorResponseError.__dict__ #later this would be a method call