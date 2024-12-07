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
            response2 = requests.post(url +"/add-item", json=data.to_json(), headers=headers)
            if response2.status_code!=200:
                logger.error(f"{response.status_code}")
    except Exception as e:
        logger.error(f"Error while trying to send an Add-Request: {e}")

def sendDeleteToDatabaseService(data:DeleteRequest):
    try:
        response = requests.post(url +"/delete-item", json=data.to_json(), headers=headers) #ToBeChanged
        if response.status_code!=200:
            response2 = requests.post(url +"/delete-item", json=data.to_json(), headers=headers)
            if response2.status_code!=200:
                logger.error(f"{response.status_code}")
    except Exception as e:
        logger.error(f"Error while trying to send a Delete-Request: {e}")


def getNextId():
    try:
        response = requests.get(url+"/get-next-id") #ToBeChanged
        if response.status_code!=200:
            response2 = requests.post(url+"/get-next-id")
            if response2.status_code!=200:
                logger.error(f"{response.status_code}")
                return None
            else:
                response_data = response2.json()
                next_id = response_data.get("id")
                if next_id is not None:
                    logger.info(f"Erhaltene ID: {next_id}")
                    return next_id
                else:
                    logger.error("Die Antwort enthält keine gültige ID.")
                    return None
        else:
            response_data = response.json()
            next_id = response_data.get("id")
            if next_id is not None:
                logger.info(f"Erhaltene ID: {next_id}")
                return next_id
            else:
                logger.error("Die Antwort enthält keine gültige ID.")
                return None
    except Exception as e:
        logger.error(f"Error while trying to send an getNextID: {e}")
        return None