from fastapi import APIRouter

from api.control.apiBF import ApiBf
from entities.models import Request, Response, AppResponse

router = APIRouter()
api_bf = ApiBf()   

@router.post("/update_products", response_model=Response)
async def init_products(request: Request):
    return api_bf.handle_update_products_request(request)

@router.get("/update_app", response_model=AppResponse)
async def update_app():
    return api_bf.handle_app_request()