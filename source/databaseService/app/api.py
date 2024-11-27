from fastapi import FastAPI
import requests

app = FastAPI()

#This interface is just for testing the connection between database- and mailing-service
#later this code shpuld be called from the interface where the data cames from the detection-service
@app.get("/testConnection")
def send_string_to_app2():
    payload = {"data": "Hello from Database-Service"}
    try:
        response = requests.post("http://mailing-service:8000/sendMail", json=payload)
        return {"status": "success", "response_from_app": response.json()}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}
