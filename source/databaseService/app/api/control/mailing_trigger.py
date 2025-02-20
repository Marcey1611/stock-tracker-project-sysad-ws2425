import os
import requests
from dotenv import load_dotenv

def trigger_mailing_service(action: str, updated_products_dict: dict):
    load_dotenv()
    mailing_service_url = os.getenv("MAILING_SERVICE_URL")

    if not mailing_service_url:
        raise ValueError("MAIL_SERVICE_URL is not set in environment variables")

    data = generate_mailing_json(updated_products_dict) if updated_products_dict else {"error_message": "An error occurred while updating products"}

    # Maximal 2 Versuche senden
    for _ in range(2):
        response = requests.post(f"{mailing_service_url}{action}", json=data)
        if response.status_code == 200:
            return
        print(f"Mailing service request failed with status {response.status_code}: {response.text}")

def generate_mailing_json(updated_products_dict: dict):
    return [item.dict() for item in updated_products_dict.values()]