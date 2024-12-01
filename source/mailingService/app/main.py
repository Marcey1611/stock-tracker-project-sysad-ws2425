from fastapi import FastAPI 
from api.boundary import api
from api.boundary import exceptionHandler


app = FastAPI()
exceptionHandler.register_exception_handlers(app)
app.include_router(api.router)