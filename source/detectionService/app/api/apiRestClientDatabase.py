import json
import logging
import requests
import os

url=os.getenv('DatabaseServiceURL') #ToBeChanged
if not url:
    url = "https://localhost:8001"

headers = {
    "Content-Type": "application/json"  # Dies sagt dem Server, dass die Daten im JSON-Format sind
}

logger = logging.getLogger('databaseRestRequests')

def addItemToDatabase(data):
    try:
        response = requests.post(url +"/add-item", json=json.dumps(data), headers=headers) #ToBeChanged
        if response.status_code!=200:
            logger.error(f"Database could not process add correctly:{str(data)}")
    except Exception as e:
        logger.error(f"Error while trying to send an Add-Request: {str(e)}")

def deleteItemFromDatabase(data):
    try:
        response = requests.post(url +"/delete-item", json=json.dumps(data), headers=headers) #ToBeChanged
        if response.status_code!=200:
            logger.error(f"Database could not process delete correctly:{str(data.getId)}")
    except Exception as e:
        logger.error(f"Error while trying to send a Delete-Request: {str(e)}")


def clearAll():
    try:
        response = requests.get(url+"/clear-all") #ToBeChanged
        if response.status_code!=200:
            logger.error(f"Database could not process getNextID correctly")
    except Exception as e:
        logger.error(f"Error while trying to send an getNextID: {str(e)}")