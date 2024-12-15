import os
import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException
from entities.UpdatedProductResponse import UpdatedProductResponse

def triggerMailingService(action: str, payload: list[UpdatedProductResponse]):
    try:
        load_dotenv()

        payload_dicts = [item.toDict() for item in payload]

        return requests.post(os.getenv("MAILING_SERVICE_URL") + action, json=payload_dicts)
    
    except RequestException as e:
        raise RequestException(f"An error occurred while triggering mailing-service: {e}")