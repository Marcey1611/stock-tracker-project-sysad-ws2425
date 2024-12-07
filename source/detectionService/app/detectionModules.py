from collections import defaultdict

from RequestModuls import AddRequest


class TrackerManager:
    def __init__(self):
        """Initialisiert die benötigten Datenstrukturen für das Tracking."""
        self.track_history = defaultdict(lambda: [])
        self.stay_time = defaultdict(lambda: 0)
        self.detected_objects = set()
        self.previous_detected_objects = set()
        self.disappearance_time = defaultdict(lambda: 0)
        self.cls_id_history = defaultdict(lambda: defaultdict(lambda: 0))
        self.rest_models = defaultdict(lambda: AddRequest(None, None, None))