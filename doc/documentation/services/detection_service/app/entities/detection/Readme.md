# detection
## detected_object
```python
class DetectedObject:
    def __init__(self, track_id, cls_id, position):
        self.track_id = track_id
        self.cls_id = cls_id
        self.position = position  # (x, y, w, h)

    def __repr__(self):
        return f"DetectedObject(ID={self.track_id}, Class={self.cls_id}, Position={self.position})"

    def get_cls_id(self):
        return self.cls_id

    def get_track_id(self):
        return self.track_id

    def set_position(self, position: (float, float, float, float)):
        self.position = position

    def get_position(self):
        return self.position

    def get_bounding_box(self):
        x, y, w, h = self.position
        x_min = x - w / 2
        y_min = y - h / 2
        x_max = x + w / 2
        y_max = y + h / 2
        return x_min, y_min, x_max, y_max
```
This class is used to keep track of a detected object.


## track_manager
```python
class TrackerManager:
    def __init__(self):
        self.track_history = defaultdict(lambda: [])
        self.stay_time = defaultdict(lambda: 0)
        self.detected_objects:dict[int,DetectedObject] = {}
        self.previous_detected_objects:dict[int,DetectedObject] = {}
        self.disappearance_time = defaultdict(lambda: 0)
        self.cls_id_history = defaultdict(lambda: defaultdict(lambda: 0))
        self.last_update = 0
```

This class is a set of Dictionaries and variables to keep track of the detected objects.