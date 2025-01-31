import logging
import requests
import os

from entities.http.database_models import DatabaseUpdateRequest

url = os.getenv('DATABASE_SERVICE_URL')  # ToBeChanged

headers = {
    "Content-Type": "application/json"  # Dies sagt dem Server, dass die Daten im JSON-Format sind
}

logger = logging.getLogger('databaseRestRequests')


def add_item_to_database(data:DatabaseUpdateRequest):
    try:
        response = requests.post(f"{url}/addItem", json=data.model_dump(), headers=headers)
        if response.status_code != 200:
            logger.error(f"Database could not process add correctly:{str(data)}")
    except Exception as e:
        logger.error(f"Error while trying to send an Add-Request: {str(e)}")


def delete_item_to_database(data:DatabaseUpdateRequest):
    try:
        response = requests.post(f"{url}/removeItem", json=data.model_dump(), headers=headers)
        if response.status_code != 200:
            logger.error(f"Database could not process delete correctly:{str(data)}")
    except Exception as e:
        logger.error(f"Error while trying to send a Delete-Request: {str(e)}")