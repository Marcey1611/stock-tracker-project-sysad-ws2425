from fastapi import APIRouter
from typing import Dict, Any

#from fastapi import FastAPI #nutzi
#from fastapi.middleware.cors import CORSMiddleware #nutzi

#app = FastAPI()  #Nutzi

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

#nutzi muss geprüft werden ob notwendig 
#app.add_middleware(
 #   CORSMiddleware,
  #  allow_origins=["*"], # oder zB auch http://localhost:8001
   # allow_credentials=True,
    #allow_methods= ["*"],
    #allow_headers= ["*"],
#)

#@app.get("/updateApp") 
#async def updateApp():
#    return {"message": "Test und halloooo"}
