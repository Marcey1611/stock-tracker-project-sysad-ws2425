from fastapi import HTTPException
from pydantic import ValidationError
from entities.httpStatusEnum import httpStatusCode

def validateAddItem(data):
    if not all([data["stockLogId"], data["productId"]]):
        raise HTTPException(status_code=httpStatusCode.BAD_REQUEST, detail="Missing required fields in addItem request.")

def validateDeleteItem(data):
    if not all([data["stockLogId"], data["productId"]]):
        raise HTTPException(status_code=httpStatusCode.BAD_REQUEST, detail="Missing required fields in deletItem request.")