import requests
from requests.exceptions import RequestException
from entities.UpdatedProductResponse import UpdatedProductResponse

def triggerMailingService(action: str, payload: list[UpdatedProductResponse]):
    print(payload.toDict())
    try:
        return requests.post("http://mailing-service:8002/" + action, json=payload.toDict())
    
    except RequestException as e:
        raise RequestException(f"An error occurred while triggering mailing-service: {e}")