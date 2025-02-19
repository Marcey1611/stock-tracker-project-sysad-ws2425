import logging
import queue
from threading import Event
from time import sleep

logger = logging.getLogger('databaseService')


def stream_frames(feed_event: Event, feed_q: queue.Queue):
    feed_event.set()
    try:
        while True:
            frame = feed_q.get()
            if frame is None:
                continue
            yield frame
            sleep(0.25)
    finally:
        feed_event.clear()