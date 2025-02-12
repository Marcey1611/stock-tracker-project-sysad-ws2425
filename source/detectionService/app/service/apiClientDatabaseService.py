import logging
import queue
from threading import Event

logger = logging.getLogger('databaseService')

def streamFeedFrames(feed_event:Event,feed_q:queue.Queue):
    feed_event.set()
    try:
        while True:
            frame = feed_q.get()
            if frame is None:
                break
            yield frame
    finally:
        feed_event.clear()

def streamTrackFrames(track_event:Event,track_q:queue.Queue):
    track_event.set()
    try:
        while True:
            frame = track_q.get()
            if frame is None:
                break
            yield frame
    finally:
        track_event.clear()