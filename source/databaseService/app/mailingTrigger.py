import requests

def triggerMail(testProductId, testProductName):
    payload = {"productId": testProductId,
               "productName": testProductName}
    try:
        response = requests.post("http://mailing-service:8000/sendMail", json=payload)
        return {"status": "successfully tested connection between database- and mailing-service", "response": response.json()}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}
    
def triggerErrorMail(errorMessage):
    payload = {"errorMessage": errorMessage}
    try:
        response = requests.post("http://mailing-service:8000/sendErrorMail", json=payload)
        return {"status": "successfully tested error connection between database- and mailing-service", "response": response.json()}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}