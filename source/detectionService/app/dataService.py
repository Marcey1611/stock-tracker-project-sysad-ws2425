import requests

from source.detectionService.app.RequestModuls import AddRequest

url="http://DataBaseService" #ToBeChanged

headers = {
    "Content-Type": "application/json"  # Dies sagt dem Server, dass die Daten im JSON-Format sind
}

def sendAddToDatabaseService(data):
    response = requests.post(url+"/add-item", json=data.toJson(), headers=headers) #ToBeChanged
    if response.status_code!=200:
        response2 = requests.post(url+"/add-item", json=data.toJson(), headers=headers)
        if response2.status_code!=200:
            print(f"Fehler: {response.status_code}")
            print(response.text)

def sendDeleteToDatabaseService(data):
    response = requests.post(url+"/delete-item", json=data.toJson(), headers=headers) #ToBeChanged
    if response.status_code!=200:
        response2 = requests.post(url+"/delete-item", json=data.toJson(), headers=headers)
        if response2.status_code!=200:
            print(f"Fehler: {response.status_code}")
            print(response.text)

def getNextId():
    response = requests.get(url+"/get-next-id") #ToBeChanged
    if response.status_code!=200:
        response2 = requests.post(url+"/get-next-id")
        if response2.status_code!=200:
            print(f"Fehler: {response.status_code}")
            print(response.text)
            return None
        else:
            print(response2.json())
            return 0
    else:
        print(response.json())
        return 0