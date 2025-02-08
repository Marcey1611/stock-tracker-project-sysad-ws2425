from fastapi import APIRouter


from api.control.apiBF import ApiBF
from entities.models import Request, Response, AppResponse

router = APIRouter()
api_bf = ApiBF()  

<<<<<<< HEAD
@router.post("/update_products", response_model=Response)
async def init_products(request: Request):
    return api_bf.handle_update_products_request(request)
=======
@router.post("/addItem", response_model=Response)
async def add_item(request: Request):
    return api_bf.handle_update_request(request, True)

@router.post("/removeItem", response_model=Response)
async def remove_item(request: Request):
    return api_bf.handle_update_request(request, False)

@router.get("/clearAll", response_model=Response)
async def clear_all():
    return api_bf.handle_reset_request()
>>>>>>> parent of d1423c4 (Merge branch 'SYSAD-71_init_request_DetectionService-&gt;DatabaseService' into 'SYSAD-87-flutter_website_connect_to_project')

@router.get("/updateApp", response_model=Dict[Any, dict])
async def update_app():
<<<<<<< HEAD
    return api_bf.handle_app_request()
=======
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
>>>>>>> parent of d1423c4 (Merge branch 'SYSAD-71_init_request_DetectionService-&gt;DatabaseService' into 'SYSAD-87-flutter_website_connect_to_project')
