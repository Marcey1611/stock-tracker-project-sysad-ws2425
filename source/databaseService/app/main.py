#Entrypoint
from fastapi import FastAPI 
from api.boundary import api

app = FastAPI()
app.include_router(api.router)

api.apiBf.addProducts(["juice", 
                    "jam", 
                    "cofffee", 
                    "water", 
                    "chocolate", 
                    "tea", 
                    "cereal", 
                    "tomato_sauce", 
                    "pasta", 
                    "chips"])