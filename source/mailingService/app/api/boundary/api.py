from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import logging

from api.control.apiBF import ApiBF
from api.validation.validator import Validator
from entity.enums import Action

router = APIRouter()
apiBF = ApiBF()
validator = Validator()

@router.post("/sendMailAdded")
async def sendMailAdded(request: Request):
    requestData = await request.json()
    validData = validator.validateData(requestData, Action.ADDED)
    return await apiBF.prepareMailingData(validData, Action.ADDED)

@router.post("/sendMailDeleted")
async def sendMailDeleted(request: Request):
    requestData = await request.json()
    validData = validator.validateData(requestData, Action.DELETED)
    return await apiBF.prepareMailingData(validData, Action.DELETED)

@router.post("/sendErrorMail")
async def sendErrorMail(request: Request):
    requestData = await request.json()
    validData = validator.validateErrorMessage(requestData)
    return await apiBF.prepareMailingDataError(validData)


   
