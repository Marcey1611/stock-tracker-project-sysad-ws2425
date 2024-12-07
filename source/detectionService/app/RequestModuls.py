class AddRequest:
    def __init__(self,dbId,cls_id,time):
        self._id=dbId
        self._cls_id=cls_id
        self._systemInTime=time

    def to_json(self):
        return {
            "id":self._id,
            "cls_id":self._cls_id,
            "self.systemInTime":self._systemInTime
        }
    @property
    def get_cls_id(self):
        return self._cls_id

    @property
    def get_id(self):
        return self._id


class DeleteRequest:
    def __init__(self, detectId, cls_id,time):
        self._id=detectId
        self._cls_id=cls_id
        self._systemOutTime=time

    @property
    def get_id(self):
        return self._id

    def to_json(self):
        return {
            "id":self._id,
            "cls_id":self._cls_id,
            "self.systemOutTime":self._systemOutTime
        }