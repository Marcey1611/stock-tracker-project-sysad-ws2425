from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "SysAdmin-Project-SS24/25"}