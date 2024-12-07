from fastapi import APIRouter, Request
from api.control.apiBF import ApiBF
from ..validation.validator import validateAddItem, validateDeleteItem

router = APIRouter()
apiBf = ApiBF()

apiBf.addProducts(["juice", 
                   "jam", 
                   "cofffee", 
                   "water", 
                   "chocolate", 
                   "tea", 
                   "cereal", 
                   "tomato_sauce", 
                   "pasta", 
                   "chips"])  

@router.post("/addItem")
async def addItem(request: Request):
    requestData = await request.json()
    validateAddItem(requestData)
    return await apiBf.addItem(requestData)

@router.post("/removeItem")
async def removeItem(request: Request):
    requestData = await request.json()
    validateDeleteItem(requestData)
    return await apiBf.removeItem(requestData)

@router.get("/getNextId")
async def getNextId():
    return await {"nextId": apiBf.getNextID()}

            