import requests
from typing import Optional
from requests.exceptions import RequestException
from entities.MailRequestModell import MailRequest
from entities.httpStatusEnum import httpStatusCode

def triggerMailingService(action: str, payload: MailRequest):
    try:
        for _ in range(2):  # Retry once if failed
            response = requests.post("http://mailing-service:8000/" + action, json=payload)

            if response["statusCode"] == 200:
                break
        
        return response
    
    except RequestException as exception:
        return {"statusCode": httpStatusCode.SERVER_ERROR, "message": str(exception)}