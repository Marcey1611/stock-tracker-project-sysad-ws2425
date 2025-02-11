from fastapi import APIRouter
import logging

from api.control.apiBF import ApiBf
from entities.models import Request, Response, AppResponse

router = APIRouter()
api_bf = ApiBf()   

logger = logging.getLogger(__name__)

@router.post("/update_products", response_model=Response)
async def init_products(request: Request):
    return api_bf.handle_update_products_request(request)

@router.get("/update_app", response_model=AppResponse)
async def update_app():
    return api_bf.handle_app_request()

@router.get("/healthcheck")
async def healthcheck():
    return {"message": "API is running"}

#do not delete! It's neccessary for the stocktracker APP
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8080", 
    "http://127.0.0.1:8080",
    "http://10.0.2.2:8001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # or http://localhost:8001
    allow_credentials=True,
    allow_methods= ["*"],
    allow_headers= ["*"],
)

app.include_router(router)
