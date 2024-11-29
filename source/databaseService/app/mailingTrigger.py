import requests

def triggerMail(testProductId, testProductName):
    payload = {"productId": testProductId,
               "productName": testProductName}
    try:
        response = requests.post("http://mailing-service:8000/sendMail", json=payload)
        return {"response": response.json()}
    except requests.exceptions.RequestException as exception:
        return {"status": "error", "message": str(exception)}
    
def triggerErrorMail(errorMessage):
    payload = {"errorMessage": errorMessage}
    try:
        response = requests.post("http://mailing-service:8000/sendErrorMail", json=payload)
        return {"response": response.json()}
    except requests.exceptions.RequestException as exception:
        return {"status": "error", "message": str(exception)}