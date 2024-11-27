from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/sendMail")
async def sendMailPostInterface(request: Request):
    try:
        data = await request.json()
        return {
            "status": "success",
            "received_data": data
        }
        #TODO Call method to send mail.
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
