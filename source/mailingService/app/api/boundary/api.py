from fastapi import APIRouter, Request

from api.control.apiBF import ApiBF
from api.validation.validator import Validator
from entity.enums import Action

router = APIRouter()

@router.post("/sendMailAdded")
async def sendMailAddedPostInterface(request: Request):
    requestData = await request.json()
    validator = Validator()
    validData = validator.validateData(requestData)
    apiBF = ApiBF()
    return await apiBF.prepareMailingData(validData, Action.ADDED)

@router.post("/sendMailDeleted")
async def sendMailDeletedPostInterface(request: Request):
    requestData = await request.json()
    validator = Validator()
    validData = validator.validateData(requestData)
    apiBF = ApiBF()
    return await apiBF.prepareMailingData(validData, Action.DELETED)

@router.post("/sendErrorMail")
async def sendErrorMailPostInterface(request: Request):
    requestData = await request.json()
    validator = Validator()
    validator.validateErrorMessage(requestData)
    validData = validator.validateData(requestData)
    apiBF = ApiBF()
    return await apiBF.prepareMailingData(validData, Action.ERROR)


   
