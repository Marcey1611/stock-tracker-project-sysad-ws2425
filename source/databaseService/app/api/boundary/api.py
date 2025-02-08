from fastapi import APIRouter
from typing import Dict, Any

from api.control.apiBF import ApiBf
from entities.models import Request, Response, AppResponse

router = APIRouter()
api_bf = ApiBf()   

@router.put("/init_products", response_model=Response)
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
    print("es funktioniert")
    return api_bf.handle_app_request()


#Nutzi für APP
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Liste der erlaubten Ursprünge (z. B. lokale Entwicklung)
origins = [
    "http://localhost:8080",  # Web-App
    "http://127.0.0.1:8080",
    "http://10.0.2.2:8001"
]

# CORS-Middleware hinzufügen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Erlaubte Ursprünge || origins
    allow_credentials=True,
    allow_methods=["*"],  # Erlaubte HTTP-Methoden
    allow_headers=["*"],  # Erlaubte Header
)

app.include_router(router)