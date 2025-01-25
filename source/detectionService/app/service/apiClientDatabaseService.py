import logging
import queue
from threading import Event

logger = logging.getLogger('databaseService')

def streamFeedFrames(feedEvent:Event,feedQ:queue.Queue):
    feedEvent.set()
    try:
        while True:
            frame = feedQ.get()
            if frame is None:
                break
            yield frame
    finally:
        feedEvent.clear()