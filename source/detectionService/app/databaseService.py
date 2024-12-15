import logging
from time import time
from typing import DefaultDict

from RequestModuls import AddRequest, DeleteRequest
from databaseRestRequests import getNextId, sendAddToDatabaseService, \
    sendDeleteToDatabaseService

logger = logging.getLogger('databaseService')

def manageAddToDatabase(rest_models:DefaultDict[int, AddRequest], added_object:int,most_frequent_cls_id:int):
    dbId=getNextId()
    reqData = AddRequest(dbId, most_frequent_cls_id, time())
    if dbId is not None:
        logger.info(f"databaseService:manageAddToDatabase: received dbID:{dbId} for track_id{added_object}")
        sendAddToDatabaseService(reqData)
    else:
        logger.error(f"databaseService:manageAddToDatabase:Error didn't receive an Id from Database for track_id{added_object}")

    if rest_models[added_object].get_id is None:
        rest_models[added_object] = reqData
    else:
        logger.error(f"databaseService:manageAddToDatabase: Error track_id{added_object} already used for new item")



def manageDeleteToDatabase(rest_models:DefaultDict[int, AddRequest], removed_object:int):
    addReq = rest_models[removed_object]
    reqData = DeleteRequest(addReq.get_id,addReq.get_cls_id,time())
    sendDeleteToDatabaseService(reqData)
    del rest_models[removed_object]
    logger.info(f"databaseService:manageDeleteToDatabase: deleted item at track_id{removed_object}")
