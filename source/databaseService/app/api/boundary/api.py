from fastapi import APIRouter
from typing import Dict, Any


from api.control.apiBF import ApiBF
from entities.models import Request, Response, AppResponse

router = APIRouter()
apiBf = ApiBF()  

@router.post("/addItem", response_model=Response)
async def addItem(request: Request):
    return apiBf.handleUpdateRequest(request, True)

@router.post("/removeItem", response_model=Response)
async def removeItem(request: Request):
    return apiBf.handleUpdateRequest(request, False)

@router.get("/clearAll", response_model=Response)
async def clearAll():
    return apiBf.handleResetRequest()

@router.get("/updateApp", response_model=Dict[Any, dict])
async def updateApp():
    return apiBf.handleAppRequest()