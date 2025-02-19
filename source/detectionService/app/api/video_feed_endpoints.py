from fastapi import APIRouter
from starlette.responses import StreamingResponse

from service.videoendpoints.frame_stream_service import stream_frames

router = APIRouter()


@router.get("/feed")
def video_feed():
    from main import feed_q, feed_event
    return StreamingResponse(stream_frames(feed_event, feed_q), media_type="multipart/x-mixed-replace; boundary=frame")


@router.get("/track")
def video_feed():
    from main import track_q, track_event
    return StreamingResponse(stream_frames(track_event, track_q),
                             media_type="multipart/x-mixed-replace; boundary=frame")
