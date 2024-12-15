import json
import logging
import requests
import os

url=os.getenv('DATABASE_SERVICE_URL') #ToBeChanged

headers = {
    "Content-Type": "application/json"  # Dies sagt dem Server, dass die Daten im JSON-Format sind
}

logger = logging.getLogger('databaseRestRequests')

def addItemToDatabase(data):
    try:
        response = requests.post(f"{url}/add-item", json=json.dumps(data), headers=headers)
        if response.status_code!=200:
            logger.error(f"Database could not process add correctly:{str(data)}")
    except Exception as e:
        logger.error(f"Error while trying to send an Add-Request: {str(e)}")

def deleteItemFromDatabase(data):
    try:
        response = requests.post(f"{url}/delete-item", json=json.dumps(data), headers=headers)
        if response.status_code!=200:
            logger.error(f"Database could not process delete correctly:{str(data.getId)}")
    except Exception as e:
        logger.error(f"Error while trying to send a Delete-Request: {str(e)}")


def clearAll():
    try:
        response = requests.get(f"{url}/clear-all")
        if response.status_code!=200:
            logger.error(f"Database could not process clearAll correctly")
    except Exception as e:
        logger.error(f"Error while trying to send an clearAll: {str(e)}")