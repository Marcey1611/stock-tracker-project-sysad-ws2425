from fastapi import APIRouter, Request, BackgroundTasks
from starlette.responses import StreamingResponse

from service.apiClientDatabaseService import videoFeedHandler

router = APIRouter()

@router.get("/feed")
async def videoFeed(request: Request, background_tasks: BackgroundTasks) -> StreamingResponse:
    from main import feedEvent, feedQ
    return videoFeedHandler(feedEvent, feedQ, request, background_tasks)


# Route for the track endpoint
@router.get("/track")
async def videoTrack(request: Request, background_tasks: BackgroundTasks) -> StreamingResponse:
    from main import trackEvent, trackQ
    return videoFeedHandler(trackEvent, trackQ, request, background_tasks)