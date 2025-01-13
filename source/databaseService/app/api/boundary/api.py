from fastapi import APIRouter
from typing import Dict, Any

from api.control.apiBF import ApiBF
from entities.models import Request, Response, AppResponse

router = APIRouter()
api_bf = ApiBF()  

@router.post("/addItem", response_model=Response)
async def add_item(request: Request):
    return api_bf.handle_update_request(request, True)

@router.post("/removeItem", response_model=Response)
async def remove_item(request: Request):
    return api_bf.handle_update_request(request, False)

@router.get("/clearAll", response_model=Response)
async def clear_all():
    return api_bf.handle_reset_request()

@router.get("/updateApp", response_model=Dict[Any, dict])
async def update_app():
    return api_bf.handle_app_request()