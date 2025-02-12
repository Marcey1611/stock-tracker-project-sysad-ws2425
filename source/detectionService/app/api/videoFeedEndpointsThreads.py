from fastapi import APIRouter, Request, BackgroundTasks
from starlette.responses import StreamingResponse

from service.apiClientDatabaseService import stream_feed_frames

router = APIRouter()

@router.get("/feed")
def videoFeed():
    from main import feedQ, feedEvent
    return StreamingResponse(stream_feed_frames(feedEvent,feedQ), media_type="multipart/x-mixed-replace; boundary=frame")



# Route for the track endpoint
@router.get("/track")
async def videoTrack() -> StreamingResponse:
    from main import trackEvent, trackQ
    return StreamingResponse(stream_feed_frames(trackEvent,trackQ), media_type="multipart/x-mixed-replace; boundary=frame")
