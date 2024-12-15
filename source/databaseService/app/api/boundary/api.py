from fastapi import APIRouter, Request
from api.control.apiBF import ApiBF
from ..validation.validator import validateRequest

router = APIRouter()
apiBf = ApiBF()  

@router.post("/addItem")
async def addItem(request: Request):
    requestData = await request.json()
    # validateRequest(requestData)
    return apiBf.addAmount(requestData)

@router.post("/removeItem")
async def removeItem(request: Request):
    requestData = await request.json()
    # validateRequest(requestData)
    return apiBf.removeAmount(requestData)

@router.get("/clearAll")
async def clearAll():
    return apiBf.resetAmounts()

            