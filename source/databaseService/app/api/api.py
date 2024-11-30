from fastapi import FastAPI, HTTPException, APIRouter
import api.mailingTrigger as mailingTrigger
#import requests
from api.validationRequest import validate_add_item, validate_delete_item
from api.modelsRequest import AddItem, DeleteItem


router = APIRouter()
'''
#TODO remove if no longer necessary (check comments below)
#This interface is just for testing the connection between database- and mailing-service
#later this code shpuld be called from the interface where the data cames from the detection-service
@app.get("/testConnection")
def testConnectionToMailingService():
    return mailingTrigger.triggerMail(1, "Product")
@app.get("/testErrorConnection")
def testErrorConnectionToMailingService():
    return mailingTrigger.triggerErrorMail("ERROR!")
'''

@router.post("/add_item")
async def add_item(data: AddItem):
    try:
        
        validate_add_item(data)
        
        print(f"Received add_item request: {data}") #ausgabe zur Prüfung
        return {"message": "Item added successfully"}

    except HTTPException as e:
        raise e


@router.post("/delete_item")
async def delete_item(data: DeleteItem):
    try:
        # Validierung der empfangenen Daten
        validate_delete_item(data)
        
        print(f"Received delete_item request: {data}") #ausgabe zur Prüfung
        return {"message": "Item deleted successfully"}

    except HTTPException as e:
        raise e
'''
@app.get("/get-next-id", response_model=NextIDResponse)
async def get_next_id_endpoint():
    
    next_id = 1  # nächste ID, als Beispiel
    print(f"Next ID available: {next_id}") #ausgabe zur Prüfung
    return NextIDResponse(nextID=next_id)
'''
            