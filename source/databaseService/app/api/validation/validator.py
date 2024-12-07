from fastapi import HTTPException
from pydantic import ValidationError
from entities.StockLogRequestModell import StockLogRequest
from entities.httpStatusEnum import httpStatusCode

def validateAddItem(data: StockLogRequest):
    if not all([data.stockLogId, data.productId, data.timeIn]):
        raise HTTPException(status_code=httpStatusCode.BAD_REQUEST, detail="Missing required fields in addItem request.")

def validateDeleteItem(data: StockLogRequest):
    if not all([data.stockLogId, data.productId, data.timeIn, data.timeOut]):
        raise HTTPException(status_code=httpStatusCode.BAD_REQUEST, detail="Missing required fields in deletItem request.")