import logging
from asyncio import sleep
import queue
from threading import Event

logger = logging.getLogger('databaseService')

def stream_feed_frames(feedEvent:Event,feedQ:queue.Queue):
    feedEvent.set()
    try:
        while True:
            frame = feedQ.get()
            if frame is None:
                sleep(0.1)
                continue
            yield frame
            sleep(0.1)
    finally:
        feedEvent.clear()
