import logging
import os
from ultralytics import YOLO
from entities.detection.track_manager import TrackerManager
from service.tracking.tracking_service import handle_disappeared_objects, update_database, update_object_tracking

logger = logging.getLogger(__name__)

file_location = "../../."+os.getenv('DETECTION_MODEL')
device = os.getenv('DEVICE_TO_RUN_MODEL')

model = YOLO(file_location).to(device)
model_cls_names = model.names

def frame_detection(frame, trackers:TrackerManager):
    results = model.track(frame, conf=0.55, imgsz=640, verbose=False,persist=True)
    annotated_frame = results[0].plot()

    current_track_ids = set()
    if results[0].boxes is not None and results[0].boxes.id is not None:
        current_track_ids = update_object_tracking(results, trackers)
    handle_disappeared_objects(current_track_ids,trackers)

    update_database(trackers,annotated_frame,frame)

    trackers.previous_detected_objects = trackers.detected_objects.copy()
    return annotated_frame