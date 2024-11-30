from fastapi import FastAPI
import requests

app = FastAPI()

#TODO remove if no longer necessary (check comments below)
#This interface is just for testing the connection between database- and mailing-service
#later this code shpuld be called from the interface where the data cames from the detection-service
@app.get("/testConnection")
def testConnectionToMailingService():
    payload = {"productId": 1,
               "productName": "testProductName",
               "productPicture": "Test-Anhang.jpg"}
    try:
        response = requests.post("http://mailing-service:8000/sendMail", json=payload)
        return {"response": response.json()}
    except requests.exceptions.RequestException as exception:
        return {"status": "error", "message": str(exception)}
    
@app.get("/testErrorConnection")
def testErrorConnectionToMailingService():
    payload = {"errorMessage": "errorMessage"}
    try:
        response = requests.post("http://mailing-service:8000/sendErrorMail", json=payload)
        return {"response": response.json()}
    except requests.exceptions.RequestException as exception:
        return {"status": "error", "message": str(exception)}
