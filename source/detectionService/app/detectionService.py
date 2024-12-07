import cv2
from cam import camera
from ultralytics import YOLO
from collections import defaultdict
import numpy as np

from databaseService import manageAddToDatabase, manageDeleteToDatabase
from RequestModuls import AddRequest
from source.detectionService.app.detectionModules import TrackerManager

# Load the YOLO11 model
model = YOLO("best.pt")

def process_frame(frame):
    results = model.track(frame, conf=0.4, persist=True, verbose=False, imgsz=640)
    annotated_frame = results[0].plot()
    return results, annotated_frame

def update_object_tracking(results, trackers, TOLERANCE, ADD_THRESHOLD):
    boxes = results[0].boxes.xywh.cpu()
    track_ids = results[0].boxes.id.int().cpu().tolist()
    cls_ids = results[0].boxes.cls.int().cpu().tolist()

    current_track_ids = set()
    for box, track_id, cls_id in zip(boxes, track_ids, cls_ids):
        x, y, w, h = map(float, box)
        current_track_ids.add(track_id)

        # Aktualisiere Klassenhistorie
        trackers.cls_id_history[track_id][cls_id] += 1

        # Berechne Entfernung und aktualisiere Verweilzeit
        if trackers.track_history[track_id]:
            last_x, last_y = trackers.track_history[track_id][-1]
            distance = ((x - last_x) ** 2 + (y - last_y) ** 2) ** 0.5
        else:
            distance = float('inf')

        if distance <= TOLERANCE:
            trackers.stay_time[track_id] += 1
        else:
            trackers.stay_time[track_id] = 0

        # Objekt hinzufügen, wenn es stabil bleibt
        if trackers.stay_time[track_id] >= ADD_THRESHOLD:
            trackers.detected_objects.add(track_id)
            trackers.disappearance_time[track_id] = 0

        # Speichere Positionshistorie
        trackers.track_history[track_id].append((x, y))
        if len(trackers.track_history[track_id]) > 30:
            trackers.track_history[track_id].pop(0)
    return current_track_ids

def handle_disappeared_objects(current_track_ids, trackers, REMOVE_THRESHOLD):
    for track_id in trackers.detected_objects.copy():
        if track_id not in current_track_ids:
            trackers['disappearance_time'][track_id] += 1
            if trackers['disappearance_time'][track_id] >= REMOVE_THRESHOLD:
                trackers.detected_objects.remove(track_id)
        else:
            trackers['disappearance_time'][track_id] = 0

def update_database(added_objects, removed_objects, trackers):
    for added_object in added_objects:
        if trackers.cls_id_history[added_object]:
            most_frequent_cls_id = max(
                trackers.cls_id_history[added_object],
                key=trackers.cls_id_history[added_object].get
            )
            manageAddToDatabase(trackers.rest_models, added_object, most_frequent_cls_id)

    for removed_object in removed_objects:
        manageDeleteToDatabase(trackers.rest_models, removed_object)

def yolo_detection():
    TOLERANCE = 10
    ADD_THRESHOLD = 1 * 30
    REMOVE_THRESHOLD = 1 * 30

    trackers = TrackerManager()

    while camera.isOpened():
        success, frame = camera.read()
        if not success:
            break

        results, annotated_frame = process_frame(frame)

        if results[0].boxes is not None and results[0].boxes.id is not None:
            current_track_ids = update_object_tracking(results, trackers, TOLERANCE, ADD_THRESHOLD)
            handle_disappeared_objects(current_track_ids, trackers, REMOVE_THRESHOLD)

            added_objects = trackers.detected_objects - trackers.previous_detected_objects
            removed_objects = trackers.previous_detected_objects - trackers.detected_objects
            update_database(added_objects, removed_objects, trackers)

            trackers.previous_detected_objects = trackers.detected_objects.copy()

        # Frame kodieren und zurückgeben
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        if not ret:
            break

        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    camera.release()
    cv2.destroyAllWindows()