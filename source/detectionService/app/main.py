from fastapi import FastAPI
import requests


app = FastAPI()

# TODO: wieder entfernen sobald test positiv

@app.get("/addItems")
def testRequestAddItems():
    payload = {
        "id": 3,
        "classID": 5,
        "SystemInTime": "2024-11-30 13:00:00",
    }
    
    try:
        response = requests.post("http://database-service:8000/add_item", json=payload)
        
        return {"response": response.json()}
    
    except requests.exceptions.RequestException as exception:
        
        return {"status": "error", "message": str(exception)}
