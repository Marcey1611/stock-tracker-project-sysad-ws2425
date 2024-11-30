from fastapi import FastAPI, Request
from ..control import apiBF

app = FastAPI()

@app.post("/sendMail")
async def sendMailPostInterface(request: Request):
    return await apiBF.prepareMailingData(request)

@app.post("/sendErrorMail")
async def sendErrorMailPostInterface(request: Request):
    return await apiBF.prepareErrorMailingData(request)
