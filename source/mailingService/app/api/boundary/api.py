from ..control import apiBF
from fastapi import APIRouter, Request
import json
from api.validation.validator import validateData, validateErrorMessage

router = APIRouter()

@router.post("/sendMail")
async def sendMailPostInterface(request: Request):
    requestData = await request.json()
    validData = validateData(requestData)
    return await apiBF.prepareMailingData(validData)

@router.post("/sendErrorMail")
async def sendErrorMailPostInterface(request: Request):
    requestData = await request.json()
    validData = validateErrorMessage(requestData)
    return await apiBF.prepareErrorMailingData(validData)


   
