from fastapi import APIRouter
from starlette.responses import StreamingResponse
from cam import generate_frames

router = APIRouter()

@router.get("/feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")