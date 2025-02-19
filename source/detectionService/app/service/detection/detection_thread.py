import logging
from multiprocessing import  Queue
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


def stream_feed_frames(frame, frame_bytes, frame_queue: Queue):
    # Wenn frame_bytes bereits vorhanden sind, verwende diese
    if frame_bytes is None:
        # Verringere die Kompressionsqualität auf z.B. 50 (niedrige Qualität)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]  # 50 ist eine geringere Qualität
        _, buffer = cv2.imencode('.jpg', frame, encode_param)
        frame_bytes = buffer.tobytes()

    try:
        # Versuche, das Bild in die Queue zu legen
        frame_queue.put_nowait(frame_bytes)  # Oder .put(), wenn du blockieren willst
    except frame_queue.full():
        # Wenn die Queue voll ist, könnte man hier eine Entscheidung treffen,
        # z.B. das älteste Bild überschreiben oder eine Warnung loggen
        print("Queue is full! Dropping the frame.")
