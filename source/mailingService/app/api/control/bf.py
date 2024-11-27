from ..entity.mailModel import Mail
from ..entity.mailErrorModel import MailError
from ..entity.mailResponseModel import MailResponse
from ..entity.mailResponseStatusEnum import Status
import json

async def prepareMailingData(sentData):
    try:
        data = await sentData.json()
        mailModel = Mail(data["productId"], data["productName"])
                
        #TODO Call method to send mail as return value.
        mailResponseSuccess = MailResponse(Status.SUCCESS, "Successfully send mail") #something like this should the called method return
        return mailResponseSuccess.__dict__ #later this would be a method call
    except Exception as e:
        mailResponseError = MailResponse(Status.ERROR, e) #something like this should the called method return
        return mailResponseError.__dict__ #later this would be a method call

async def prepareErrorMailingData(sentData):
    try:
        data = await sentData.json()
        mailErrorModel = MailError(data["errorMessage"])
                
        #TODO Call method to send mail as return value.
        mailResponseSuccess = MailResponse(Status.SUCCESS, "Successfull send error mail") #something like this should the called method return
        return mailResponseSuccess.__dict__ #later this would be a method call
    except Exception as exception:
        mailResponseError = MailResponse(Status.ERROR, "ERROR") #something like this should the called method return
        return mailResponseError.__dict__ #later this would be a method call