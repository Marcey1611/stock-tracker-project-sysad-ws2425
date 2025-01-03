from collections import defaultdict

from entities.detection.detectedObject import DetectedObject

class TrackerManager:
    def __init__(self):
        self.trackHistory = defaultdict(lambda: [])
        self.stayTime = defaultdict(lambda: 0)
        self.detectedObjects = defaultdict(lambda : DetectedObject(None,None,None))
        self.previousDetectedObjects = defaultdict(lambda : DetectedObject(None,None,None))
        self.disappearanceTime = defaultdict(lambda: 0)
        self.clsIdHistory = defaultdict(lambda: defaultdict(lambda: 0))