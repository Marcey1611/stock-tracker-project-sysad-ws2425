import logging
import requests
import os

from entities.http.database_models import DatabaseUpdateRequest

url = os.getenv('DATABASE_SERVICE_URL')

headers = {
    "Content-Type": "application/json"
}

logger = logging.getLogger('databaseRestRequests')


def update_database_products(data:DatabaseUpdateRequest):
    try:
        response = requests.post(f"{url}/update_products", json=data.model_dump(), headers=headers)
        if response.status_code != 200:
            logger.error(f"Database could not process correctly:{str(data.model_dump())}")
        return True
    except Exception as e:
        logger.error(f"Error while trying to send a Request: {str(e)}")
        return False