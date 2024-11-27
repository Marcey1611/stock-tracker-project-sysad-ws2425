import requests

def triggerMail(testProductId, testProductName):
    payload = {"productId": testProductId,
               "productName": testProductName}
    try:
        response = requests.post("http://mailing-service:8000/sendMail", json=payload)
        return {"status": "success", "response": response.json()}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}