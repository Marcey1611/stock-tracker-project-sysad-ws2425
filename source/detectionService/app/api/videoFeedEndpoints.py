from fastapi import APIRouter
from starlette.responses import StreamingResponse
from camera.cam import streamFrames
from service.detection.detectionService import yoloDetection

router = APIRouter()

@router.get("/feed")
def videoFeed():
    return StreamingResponse(streamFrames(), media_type="multipart/x-mixed-replace; boundary=frame")
@router.get("/track")
def videoTrack():
    return StreamingResponse(yoloDetection(), media_type="multipart/x-mixed-replace; boundary=frame")