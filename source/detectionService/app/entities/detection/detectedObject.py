class DetectedObject:
    def __init__(self, trackId, clsId, position):
        self.trackId = trackId
        self.clsId = clsId
        self.position = position  # (x, y, w, h)

    def __repr__(self):
        return f"DetectedObject(ID={self.trackId}, Class={self.clsId}, Position={self.position})"

    def getClsId(self):
        return self.clsId
    def getTrackId(self):
        return self.trackId
    def setPosition(self,position:(float,float,float,float)):
        self.position = position
    def getPosition(self):
        return self.position