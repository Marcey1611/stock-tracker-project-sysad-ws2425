from collections import defaultdict

from entities.detection.detected_object import DetectedObject


class TrackerManager:
    def __init__(self):
        self.track_history = defaultdict(lambda: [])
        self.stay_time = defaultdict(lambda: 0)
        self.detected_objects:dict[int,DetectedObject] = {}
        self.previous_detected_objects:dict[int,DetectedObject] = {}
        self.disappearance_time = defaultdict(lambda: 0)
        self.cls_id_history = defaultdict(lambda: defaultdict(lambda: 0))
        self.last_update = 0
