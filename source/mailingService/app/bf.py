from mailModel import Mail
from mailErrorModel import MailError

async def prepareMailingData(sentData):
    try:
        data = await sentData.json()
        mailModel = Mail(data["productId"], data["productName"])
                
        #TODO Call method to send mail as return value.
        return {"status": "successfully received data"}
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

async def prepareErrorMailingData(sentData):
    try:
        data = await sentData.json()
        mailErrorModel = MailError(data["errorMessage"])
                
        #TODO Call method to send mail as return value.
        return {"status": "successfully received error data"}
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }