from fastapi import APIRouter, Request

from api.control import apiBF
from api.validation import validator

router = APIRouter()

@router.post("/sendMail")
async def sendMailPostInterface(request: Request):
    requestData = await request.json()
    validData = validator.validateData(requestData)
    return await apiBF.prepareMailingData(validData)

@router.post("/sendErrorMail")
async def sendErrorMailPostInterface(request: Request):
    requestData = await request.json()
    validData = validator.validateErrorMessage(requestData)
    return await apiBF.prepareErrorMailingData(validData)


   
