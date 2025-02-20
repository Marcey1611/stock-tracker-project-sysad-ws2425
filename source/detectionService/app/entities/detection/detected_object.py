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
