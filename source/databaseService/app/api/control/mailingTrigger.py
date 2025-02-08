import json
import os
import requests
from dotenv import load_dotenv


def trigger_mailing_service(action: str, updated_products_dict: dict):
    load_dotenv()

    # Send request | Retry once if response is not 200
    for _ in range(2):
        if updated_products_dict:
            mailing_service_response = requests.post(os.getenv("MAILING_SERVICE_URL") + action, json=generate_mailing_json(updated_products_dict))
            if mailing_service_response.status_code == 200: break
        else:
            mailing_service_response = requests.post(os.getenv("MAILING_SERVICE_URL") + action, json="An error occurred while updating products")
            if mailing_service_response.status_code == 200: break

def generate_mailing_json(updated_products_dict: dict):
    serialized_data = [item.dict() for item in updated_products_dict.values()]
    return serialized_data