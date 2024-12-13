from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from api.control.apiBF import ApiBF
from api.validation.validator import Validator
from entity.enums import Action

router = APIRouter()
apiBF = ApiBF()
validator = Validator()

@router.post("/sendMailAdded")
async def sendMailAddedPostInterface(request: Request):
    #requestData = await request.json()
    #validData = validator.validateData(requestData, True)
    return JSONResponse(content={"message": "Successfully send mail"}, status_code=200)

    #return await apiBF.prepareMailingData(validData, Action.ADDED)

@router.post("/sendMailDeleted")
async def sendMailDeletedPostInterface(request: Request):
    requestData = await request.json()
    validData = validator.validateData(requestData, True)
    return await apiBF.prepareMailingData(validData, Action.DELETED)

@router.post("/sendErrorMail")
async def sendErrorMailPostInterface(request: Request):
    requestData = await request.json()
    validData = validator.validateData(requestData, False)
    return await apiBF.prepareMailingData(validData, Action.ERROR)


   
