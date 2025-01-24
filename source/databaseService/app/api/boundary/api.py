from fastapi import APIRouter
from typing import Dict, Any

from api.control.apiBF import ApiBf
from entities.models import Request, Response, AppResponse

router = APIRouter()
api_bf = ApiBf()   

@router.post("/init_products", response_model=Response)
async def init_products(request: Request):
    return api_bf.handle_init_products_request(request)

@router.post("/add_item", response_model=Response)
async def add_item(request: Request):
    return api_bf.handle_update_request(request, True)

@router.post("/remove_item", response_model=Response)
async def remove_item(request: Request):
    return api_bf.handle_update_request(request, False)

@router.get("/clear_all", response_model=Response)
async def clear_all():
    return api_bf.handle_reset_request()

@router.get("/update_app", response_model=AppResponse)
async def update_app():
    return api_bf.handle_app_request()