from fastapi import FastAPI
from routesVideo import router as video_router

app = FastAPI()

app.include_router(video_router, prefix="/video", tags=["video"])

@app.get("/")
def read_root():
    return {"message": "SysAdmin-Project-SS24/25"}