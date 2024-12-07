import logging
import requests
import os


from RequestModuls import AddRequest, DeleteRequest

url=os.getenv('DatabaseServiceURL') #ToBeChanged

headers = {
    "Content-Type": "application/json"  # Dies sagt dem Server, dass die Daten im JSON-Format sind
}

logger = logging.getLogger('databaseRestRequests')

def sendAddToDatabaseService(data:AddRequest):
    try:
        response = requests.post(url +"/add-item", json=data.to_json(), headers=headers) #ToBeChanged
        if response.status_code!=200:
            logger.error(f"Database could not process add correctly:{data.get_id}")
    except Exception as e:
        logger.error(f"Error while trying to send an Add-Request: {e}")

def sendDeleteToDatabaseService(data:DeleteRequest):
    try:
        response = requests.post(url +"/delete-item", json=data.to_json(), headers=headers) #ToBeChanged
        if response.status_code!=200:
            logger.error(f"Database could not process delete correctly:{data.get_id}")
    except Exception as e:
        logger.error(f"Error while trying to send a Delete-Request: {e}")


def getNextId():
    try:
        response = requests.get(url+"/get-next-id") #ToBeChanged
        if response.status_code!=200:
            logger.error(f"Database could not process getNextID correctly")
        else:
            response_data = response.json()
            next_id = response_data.get("id")
            if next_id is not None:
                logger.info(f"received ID: {next_id}")
                return next_id
            else:
                logger.error("Could not receive a valid ID.")
                return None
    except Exception as e:
        logger.error(f"Error while trying to send an getNextID: {e}")
        return None