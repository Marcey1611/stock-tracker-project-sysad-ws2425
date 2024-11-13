# app/main.py
from fastapi import FastAPI

app = FastAPI()

# Platzhalter-Interface
@app.get("/")
def read_root():
    return {"message": "SysAdmin-Project-SS24/25"}