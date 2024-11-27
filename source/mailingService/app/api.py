from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/sendMail")
async def receive_string(request: Request):
    data = await request.json()
    received_data = data.get("data", "No data received")
    return {"message": f"App 2 received: {received_data}"}
