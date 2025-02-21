# Tracking
## [tracking_service.py](../../../../../../../source/detectionService/app/service/tracking/tracking_service.py)
This file handels updating the [TrackingManager](../../entities/detection/Readme.md). 
### update_object_tracking
```python
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

            trackers.cls_id_history[track_id][cls_id] += 1

            if trackers.track_history[track_id]:
                lastX, lastY = trackers.track_history[track_id][-1]
                distance = ((x - lastX) ** 2 + (y - lastY) ** 2) ** 0.5
            else:
                distance = float('inf')

            if distance <= TOLERANCE:
                trackers.stay_time[track_id] += 1
            else:
                trackers.stay_time[track_id] = 0

            if trackers.stay_time[track_id] >= ADD_REMOVE_THRESHOLD:
                position = (x, y, w, h)
                trackers.detected_objects[track_id] = DetectedObject(track_id, cls_id, position)
                trackers.disappearance_time[track_id] = 0

            trackers.track_history[track_id].append((x, y))
            if len(trackers.track_history[track_id]) > 30:
                trackers.track_history[track_id].pop(0)
    return current_track_ids
```
ChatGPT heavily influenced this code.
It allows us to add the [Detected Products](../../entities/detection/Readme.md) to the 
[TrackingManager](../../entities/detection/Readme.md) if they stand still.
Additionally, it saves the bounding box for the [Drawings](../../entities/detection/Readme.md) done later  

ChatGPT heavily influences this code.
### handle_disappeared_objects
```python
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
```
This Methode does remove disappeared objects.
If the Object is disappeared longer than the ADD_REMOVE_THRESHOLD allows it to, then the object will be removed from the [trackers.detected_objects](../../entities/detection/Readme.md) dictionary.

### update_database
```python
def update_database(trackers: TrackerManager, annotated_frame, frame):
    current_time = time.monotonic()
    if len(trackers.detected_objects.items())!=len(trackers.previous_detected_objects.items()) or current_time-trackers.last_update > UPDATE_INTERVALL:
        if len(trackers.detected_objects.items())==0 and len(trackers.previous_detected_objects.items())>1:
            generate_http_request(trackers, annotated_frame, None)
        else:
            generate_http_request(trackers, annotated_frame, frame)
        trackers.last_update = current_time
```
This Code checks if the previously detected objects and the detected objects differ.
Additionally, it checks if the last update is larger than the UPDATE_INTERVALL.
If one is the case, it will start triggering the [Request to the database](../http_request/Readme.md).