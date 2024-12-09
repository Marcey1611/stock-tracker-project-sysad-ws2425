from fastapi import APIRouter, Request
from api.control.apiBF import ApiBF
from ..validation.validator import validateAddItem, validateDeleteItem

router = APIRouter()
apiBf = ApiBF()  

@router.post("/addItem")
async def addItem(request: Request):
    requestData = await request.json()
    validateAddItem(requestData)
    return apiBf.addItem(requestData)

@router.post("/removeItem")
async def removeItem(request: Request):
    requestData = await request.json()
    validateDeleteItem(requestData)
    return apiBf.removeItem(requestData)

@router.get("/getNextId")
async def getNextId():
    return {"nextId": apiBf.getNextID()}

            