from dataService import getNextId
from time import time
class AddRequest:
    def __init__(self,cls_id):
        self.id=getNextId()
        self.cls_id=cls_id
        self.systemInTime=time() #ToBeChanged

    def toJson(self):
        return {
            "id":self.id,
            "cls_id":self.cls_id,
            "self.systemInTime":self.systemInTime
        }

class DeleteRequest:
    def __init__(self, detectId, cls_id):
        self.id=detectId
        self.cls_id=cls_id
        self.systemOutTime=time()
    @classmethod
    def fromAddRequest(cls,add:AddRequest):
        cls(add.id,add.cls_id)

    def toJson(self):
        return {
            "id":self.id,
            "cls_id":self.cls_id,
            "self.systemInTime":self.systemOutTime
        }
# entferne noch die methoden
# nur getter setter und constuctor