import logging
import requests
import os


from moduls.requestModuls import AddRequest, DeleteRequest

url=os.getenv('DatabaseServiceURL') #ToBeChanged

headers = {
    "Content-Type": "application/json"  # Dies sagt dem Server, dass die Daten im JSON-Format sind
}

logger = logging.getLogger('databaseRestRequests')

def addItemToDatabase(data:AddRequest):
    try:
        response = requests.post(url +"/add-item", json=data.toJson(), headers=headers) #ToBeChanged
        if response.status_code!=200:
            logger.error(f"Database could not process add correctly:{data.getId}")
    except Exception as e:
        logger.error(f"Error while trying to send an Add-Request: {str(e)}")

def deleteItemFromDatabase(data:DeleteRequest):
    try:
        response = requests.post(url +"/delete-item", json=data.toJson(), headers=headers) #ToBeChanged
        if response.status_code!=200:
            logger.error(f"Database could not process delete correctly:{data.getId}")
    except Exception as e:
        logger.error(f"Error while trying to send a Delete-Request: {str(e)}")


def fetchNextDatabaseId():
    try:
        response = requests.get(url+"/get-next-id") #ToBeChanged
        if response.status_code!=200:
            logger.error(f"Database could not process getNextID correctly")
        else:
            response_data = response.json()
            nextId = response_data.get("id")
            if nextId is not None:
                logger.info(f"received ID: {nextId}")
                return nextId
            else:
                logger.error("Could not receive a valid ID.")
                return None
    except Exception as e:
        logger.error(f"Error while trying to send an getNextID: {str(e)}")
        return None