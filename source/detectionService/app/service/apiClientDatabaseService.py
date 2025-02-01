import logging
from fastapi import Request, BackgroundTasks
from fastapi.responses import StreamingResponse
import queue
from threading import Event
from typing import Generator

logger = logging.getLogger('databaseService')


def streamFeedFrames(feedEvent: Event, feedQ: queue.Queue, stop_event: Event) -> Generator[bytes, None, None]:
    """
    Streams frames from the feed queue, yielding each frame.
    Stops streaming when the user disconnects or the queue is empty.

    Parameters:
        feedEvent (Event): A threading event used to control the stream.
        feedQ (queue.Queue): A queue containing the video frames to be streamed.
        stop_event (Event): An event used to stop the stream when the client disconnects.

    Yields:
        bytes: The video frame in the form of bytes.
    """
    feedEvent.set()  # Set the event to indicate the feed is active

    try:
        while not stop_event.is_set():  # Check if the stop event is set (indicating disconnect)
            try:
                # Get the next frame from the queue with a timeout of 1 second
                frame = feedQ.get_nowait()
                if frame is None:
                    break  # Exit if None is received (e.g., end of stream signal)
                yield frame  # Yield the frame to the response stream
            except queue.Empty:
                continue  # If the queue is empty, continue to the next loop iteration
    finally:
        feedEvent.clear()  # Ensure the event is cleared after the streaming ends


def monitor_disconnect(request: Request, stop_event: Event):
    """
    Monitors the connection and sets the stop_event when the client disconnects.

    Parameters:
        request (Request): The FastAPI request object to check for disconnect status.
        stop_event (Event): An event to signal when the client disconnects.
    """
    # Loop and check if the client is disconnected
    while True:
        if request.is_disconnected:
            stop_event.set()  # Set the stop event when the client disconnects
            break


# General endpoint handler for any video feed
def videoFeedHandler(event: Event, queue: queue.Queue, request: Request,
                     background_tasks: BackgroundTasks) -> StreamingResponse:
    """
    A reusable function to stream video feeds using the provided event and queue.

    Parameters:
        event (Event): The threading event controlling the feed.
        queue (Queue): The queue containing the frames.
        request (Request): The FastAPI request object to check for disconnect status.
        background_tasks (BackgroundTasks): The background tasks manager to monitor disconnections.

    Returns:
        StreamingResponse: The response object to stream frames.
    """
    # Create a stop event to be used to stop streaming if the client disconnects
    stop_event = Event()

    # Run the disconnection monitor in the background
    background_tasks.add_task(monitor_disconnect, request, stop_event)

    # Return the StreamingResponse with the frames, stopping when stop_event is set
    return StreamingResponse(streamFeedFrames(event, queue, stop_event),
                             media_type="multipart/x-mixed-replace; boundary=frame")

