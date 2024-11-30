from fastapi import FastAPI
import requests


app = FastAPI()

# TODO: wieder entfernen sobald testreihe positiv
'''
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
'''
'''         
#zweiter Datensatz
@app.get("/addItems")
def testRequestAddItems():
    payload = {
        "id": 7,
        "classID": 2,
        "SystemInTime": "2024-11-30 14:40:00",
    }
    try:
        response = requests.post("http://database-service:8000/add_item", json=payload)  
        return {"response": response.json()}
    except requests.exceptions.RequestException as exception:  
        return {"status": "error", "message": str(exception)}
'''
'''
@app.get("/deleteItems")
def testRequestDeleteItems():
    payload = {
        "id": 3,
        "classID": 5,
        "SystemOutTime": "2024-11-30 14:45:00",
    }
    try:
        response = requests.post("http://database-service:8000/delete_item", json=payload)  
        return {"response": response.json()}
    except requests.exceptions.RequestException as exception:  
        return {"status": "error", "message": str(exception)}
''' 

@app.get("/getNextID")

def testRequestGetNextID():
    try:
        response = requests.get("http://database-service:8000/get_next_id")
        return {"response": response.json()}
    except requests.exceptions.RequestException as exception:  
        return {"status": "error", "message": str(exception)}

