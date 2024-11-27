from fastapi import FastAPI
import mailingTrigger
import requests

app = FastAPI()

#TODO remove if no longer necessary (check comments below)
#This interface is just for testing the connection between database- and mailing-service
#later this code shpuld be called from the interface where the data cames from the detection-service
@app.get("/testConnection")
def testConnectionToMailingService():
    return mailingTrigger.triggerMail(1, "Product")
