from collections import defaultdict

from source.detectionService.app.api.moduls.requestModuls import AddRequest


class TrackerManager:
    def __init__(self):
        self.trackHistory = defaultdict(lambda: [])
        self.stayTime = defaultdict(lambda: 0)
        self.detectedObjects = set()
        self.previousDetectedObjects = set()
        self.disappearanceTime = defaultdict(lambda: 0)
        self.clsIdHistory = defaultdict(lambda: defaultdict(lambda: 0))
        self.restModels = defaultdict(lambda: AddRequest(None, None, None))