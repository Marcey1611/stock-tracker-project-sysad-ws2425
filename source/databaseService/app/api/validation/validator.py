from fastapi import HTTPException
from pydantic import ValidationError
from entities.httpStatusEnum import httpStatusCode

def validateRequest(data):
    if "ids" not in data or not isinstance(data["ids"], list):
        raise HTTPException(
            status_code=httpStatusCode.BAD_REQUEST, 
            detail="Missing required 'ids' array in request or 'ids' is not a list."
        )