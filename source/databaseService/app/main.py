#Entrypoint
from fastapi import FastAPI 
from api.boundary import api

app = FastAPI()
app.include_router(api.router)