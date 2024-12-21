import os
import requests
from dotenv import load_dotenv

def triggerMailingService(action: str, updatedProductsDict: dict):
    load_dotenv()

    # Convert dict to Json payload
    json_payload = {key: value.dict() for key, value in updatedProductsDict.items()}

    # Send request | Retry once if response is not 200
    for _ in range(2):
        mailingServiceResponse = requests.post(os.getenv("MAILING_SERVICE_URL") + action, json=json_payload)
        if mailingServiceResponse.status_code == 200: break