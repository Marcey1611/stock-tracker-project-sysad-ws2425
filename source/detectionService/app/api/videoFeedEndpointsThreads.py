from fastapi import APIRouter
from starlette.responses import StreamingResponse

from service.apiClientDatabaseService import streamFeedFrames

router = APIRouter()

@router.get("/feed")
def videoFeed():
    from main import feedQ, feedEvent
    return StreamingResponse(streamFeedFrames(feedEvent,feedQ), media_type="multipart/x-mixed-replace; boundary=frame")
@router.get("/track")
def videoFeed():
    from main import trackEvent, trackQ
    return StreamingResponse(streamFeedFrames(trackEvent,trackQ), media_type="multipart/x-mixed-replace; boundary=frame")