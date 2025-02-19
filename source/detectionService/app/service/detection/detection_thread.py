import logging
import queue
from threading import Event
import cv2

from entities.detection.track_manager import TrackerManager
from service.detection.frame_processess import process_frame
from service.detection.human_check import is_human_in_frame


logger = logging.getLogger(__name__)

def detection(feed_event:Event,feed_q:queue.Queue,track_event:Event,track_q:queue.Queue,frame,frame_bytes,trackers:TrackerManager):

    human_check, annotated_frame = is_human_in_frame(frame)
    if human_check:
        if feed_event.is_set():
            stream_feed_frames(frame, frame_bytes, feed_q)
        if track_event.is_set():
            stream_feed_frames(annotated_frame, None, track_q)

    else:
        annotated_frame = process_frame(frame, trackers)

        if feed_event.is_set():
            stream_feed_frames(frame, frame_bytes, feed_q)
        if track_event.is_set():
            stream_feed_frames(annotated_frame, None, track_q)


def stream_feed_frames(frame, frame_bytes, feed_q: queue.Queue):
    if frame_bytes is None:
        _, buffer = cv2.imencode('.jpeg', frame)
        frame_bytes = buffer.tobytes()
        feed_q.put_nowait(b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')