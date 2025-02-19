import time

from entities.detection.detected_object import DetectedObject
from entities.detection.track_manager import TrackerManager
from service.http_request.http_request_service import http_request_service

TOLERANCE = 10
ADD_REMOVE_THRESHOLD = .5 * 30
UPDATE_INTERVALL = 15

def update_object_tracking(results, trackers: TrackerManager):
    boxes = results[0].boxes.xywh.cpu()
    track_ids = results[0].boxes.id.int().cpu().tolist()
    cls_ids = results[0].boxes.cls.int().cpu().tolist()

    current_track_ids = set()
    for box, track_id, cls_id in zip(boxes, track_ids, cls_ids):
        x, y, w, h = map(float, box)
        current_track_ids.add(track_id)
        if any(obj.get_track_id() == track_id for obj in trackers.previous_detected_objects.values()):
            trackers.previous_detected_objects[track_id].position = (x, y, w, h)
            trackers.detected_objects[track_id] = trackers.previous_detected_objects[track_id]
        else :
            # Aktualisiere Klassenhistorie
            trackers.cls_id_history[track_id][cls_id] += 1

            # Berechne Entfernung und aktualisiere Verweilzeit
            if trackers.track_history[track_id]:
                lastX, lastY = trackers.track_history[track_id][-1]
                distance = ((x - lastX) ** 2 + (y - lastY) ** 2) ** 0.5
            else:
                distance = float('inf')

            if distance <= TOLERANCE:
                trackers.stay_time[track_id] += 1
            else:
                trackers.stay_time[track_id] = 0

            # Objekt hinzufügen, wenn es stabil bleibt
            if trackers.stay_time[track_id] >= ADD_REMOVE_THRESHOLD:
                position = (x, y, w, h)
                trackers.detected_objects[track_id] = DetectedObject(track_id, cls_id, position)
                trackers.disappearance_time[track_id] = 0

            # Speichere Positionshistorie
            trackers.track_history[track_id].append((x, y))
            if len(trackers.track_history[track_id]) > 30:
                trackers.track_history[track_id].pop(0)
    return current_track_ids


def handle_disappeared_objects(current_track_ids, trackers: TrackerManager):
    to_remove = []

    for _, detectOb in trackers.detected_objects.items():
        track_id = detectOb.get_track_id()
        if track_id not in current_track_ids:
            trackers.disappearance_time[track_id] += 1
            if trackers.disappearance_time[track_id] >= ADD_REMOVE_THRESHOLD:
                to_remove.append(track_id)
        else:
            trackers.disappearance_time[track_id] = 0

    for track_id in to_remove:
        del trackers.detected_objects[track_id]


def update_database(trackers: TrackerManager, annotated_frame, frame):
    current_time = time.monotonic()
    if len(trackers.detected_objects.items())!=len(trackers.previous_detected_objects.items()) or current_time-trackers.last_update > UPDATE_INTERVALL:
        if len(trackers.detected_objects.items())==0 and len(trackers.previous_detected_objects.items())>1:
            http_request_service(trackers,annotated_frame,None)
        else:
            http_request_service(trackers,annotated_frame,frame)
        trackers.last_update = current_time