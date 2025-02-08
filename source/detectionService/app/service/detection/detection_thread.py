import copy
import logging
import queue
import time
from threading import Event
import cv2

import service.detection.frame_processess as frame_processing
from entities.detection.track_manager import TrackerManager
from service.detection.human_check import is_human_in_frame
from service.http_request.http_request_service import init_database
from service.tracking.tracking_service import handle_disappeared_objects, update_database, update_object_tracking
from ultralytics import YOLO


logger = logging.getLogger('detectionThread')
model = YOLO("./service/detection/yolo11l.pt")
model_cls_names = model.names


def detection_thread(feed_event: Event, feed_q: queue.Queue, track_event: Event, track_q: queue.Queue, source):
    camera = cv2.VideoCapture(source)
    if camera.isOpened():
        logger.info(f"Camera {source} opend.")
    else:
        logger.error(f"Could not open camera:{source}.")
        return
    init_cam(camera, source)

    _, frame = camera.read()
    init_database(frame,model)
    init_done = False
    while init_done is False:
        init_done = init_database(frame,model)
        if init_done is False:
            logger.info("Try Connecting to Database-Service in 5 ...")
            time.sleep(5)


    trackers = TrackerManager()

    while True:
        success, frame = camera.read()  # Frame von der Kamera lesen
        if not success:
            logger.error("Error could not access camera frame.")
            break
        else:
            human_check, annotated_frame = is_human_in_frame(frame)
            if human_check:
                if feed_event.is_set():
                    put_frames_into_queue(frame, feed_q)
                if track_event.is_set():
                    put_frames_into_queue(annotated_frame, track_q)
            else:
                annotated_frame = process_frame(frame, trackers)

                if feed_event.is_set():
                    put_frames_into_queue(frame, feed_q)
                if track_event.is_set():
                    put_frames_into_queue(annotated_frame, track_q)

    camera.release()
    logger.info(f"Camera {source} closed.")

def process_frame(frame, trackers: TrackerManager):
    results = model.track(frame, conf=0.55, imgsz=640, verbose=False)
    annotated_frame = results[0].plot()

    current_track_ids = set()
    if results[0].boxes is not None and results[0].boxes.id is not None:
        current_track_ids = update_object_tracking(results, trackers)
    handle_disappeared_objects(current_track_ids, trackers)

    update_database(trackers, annotated_frame,frame)

    trackers.previous_detected_objects = copy.deepcopy(trackers.detected_objects)

    return annotated_frame

def put_frames_into_queue(frame, feed_queue: queue.Queue):
    _, buffer = cv2.imencode('.webp', frame)
    frame_bytes = buffer.tobytes()
    feed_queue.put(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def init_cam(camera: cv2.VideoCapture, source):
    desired_width = 1920
    desired_height = 1080

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YUYV'))

    frame_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
    logger.debug(f"Camera resolution:{str(source)}: {int(frame_width)}x{int(frame_height)}")