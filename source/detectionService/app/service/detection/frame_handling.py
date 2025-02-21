import logging
from multiprocessing import  Queue
from threading import Event
import cv2

from entities.detection.track_manager import TrackerManager
from service.detection.frame_detecting import frame_detection
from service.detection.human_checking import is_human_in_frame


logger = logging.getLogger(__name__)

def frame_handling(feed_q:Queue, track_q:Queue, frame, frame_bytes, trackers:TrackerManager):

    human_check, annotated_frame = is_human_in_frame(frame)
    if human_check:
        put_frames_into_queue(frame, frame_bytes, feed_q)
        put_frames_into_queue(annotated_frame, None, track_q)

    else:
        annotated_frame = frame_detection(frame, trackers)

        put_frames_into_queue(frame, frame_bytes, feed_q)
        put_frames_into_queue(annotated_frame, None, track_q)


def put_frames_into_queue(frame, frame_bytes, frame_queue: Queue):
    if frame_bytes is None:
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
        _, buffer = cv2.imencode('.jpg', frame, encode_param)
        frame_bytes = buffer.tobytes()

    try:
        if frame_queue.full():
            frame_queue.get_nowait()
        frame_queue.put_nowait(frame_bytes)
    except Exception as e:
        print(f"Error while putting frame in queue: {e}")