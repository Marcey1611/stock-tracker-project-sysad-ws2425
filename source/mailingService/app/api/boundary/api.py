from fastapi import FastAPI, Request
from ..control import bf

app = FastAPI()

@app.post("/sendMail")
async def sendMailPostInterface(request: Request):
    return await bf.prepareMailingData(request)

@app.post("/sendErrorMail")
async def sendErrorMailPostInterface(request: Request):
    return await bf.prepareErrorMailingData(request)
