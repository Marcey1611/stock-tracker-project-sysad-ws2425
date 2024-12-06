#Entrypoint
from fastapi import FastAPI 
from api import api

app = FastAPI()
app.include_router(api.router)