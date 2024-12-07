class AddRequest:
    def __init__(self,dbId,clsId,time):
        self._id=dbId
        self._clsId=clsId
        self._systemInTime=time

    def toJson(self):
        return {
            "id":self._id,
            "clsId":self._clsId,
            "self.systemInTime":self._systemInTime
        }
    @property
    def getClsId(self):
        return self._clsId

    @property
    def getId(self):
        return self._id


class DeleteRequest:
    def __init__(self, detectId, clsId,time):
        self._id=detectId
        self._clsId=clsId
        self._systemOutTime=time

    @property
    def getId(self):
        return self._id

    def toJson(self):
        return {
            "id":self._id,
            "clsId":self._clsId,
            "self.systemOutTime":self._systemOutTime
        }