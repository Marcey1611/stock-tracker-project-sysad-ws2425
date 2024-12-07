import logging
from time import time
from typing import DefaultDict

from ..api.moduls.requestModuls import AddRequest, DeleteRequest
from ..api.apiRestClientDatabase import fetchNextDatabaseId, addItemToDatabase, \
    deleteItemFromDatabase

logger = logging.getLogger('databaseService')

def manageAddToDatabase(restModels:DefaultDict[int, AddRequest], addedObject:int, mostFrequentClsId:int):
    dbId=fetchNextDatabaseId()
    reqData = AddRequest(dbId, mostFrequentClsId, time())
    if dbId is not None:
        logger.info(f"databaseService:manageAddToDatabase: received dbID:{dbId} for trackId{addedObject}")
        addItemToDatabase(reqData)
    else:
        logger.error(f"databaseService:manageAddToDatabase:Error didn't receive an Id from Database for trackId{addedObject}")

    if restModels[addedObject].getId is None:
        restModels[addedObject] = reqData
    else:
        logger.error(f"databaseService:manageAddToDatabase: Error trackId{addedObject} already used for new item")



def manageDeleteToDatabase(restModels:DefaultDict[int, AddRequest], removedObject:int):
    addReq = restModels[removedObject]
    reqData = DeleteRequest(addReq.getId,addReq.getClsId,time())
    deleteItemFromDatabase(reqData)
    del restModels[removedObject]
    logger.info(f"databaseService:manageDeleteToDatabase: deleted item at trackId{removedObject}")
