import json
import os
import requests
from dotenv import load_dotenv


def triggerMailingService(action: str, updatedProductsDict: dict):
    load_dotenv()

    # Send request | Retry once if response is not 200
    #for _ in range(2):
     #   mailingServiceResponse = requests.post(os.getenv("MAILING_SERVICE_URL") + action, json=generateMailingJSON(updatedProductsDict))
      #  if mailingServiceResponse.status_code == 200: break

def generateMailingJSON(updatedProductsDict: dict):
    serializedData = [item.dict() for item in updatedProductsDict.values()]
    return serializedData