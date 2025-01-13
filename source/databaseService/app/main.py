#Entrypoint
import logging
from fastapi import FastAPI 
from api.boundary import api

app = FastAPI()
app.include_router(api.router)

api.api_bf.handle_create_request(["juice", 
                    "jam", 
                    "cofffee", 
                    "water", 
                    "chocolate", 
                    "tea", 
                    "cereal", 
                    "tomato_sauce", 
                    "pasta", 
                    "chips"])