import json
from typing import Dict, Any
from fastapi import HTTPException


def validateData(data: Dict[str, Any]) -> Dict[str, Any]:
    productIdMissing = "productId" not in data
    productNameMissing = "productName" not in data
    productPictureMissing = "productPicture" not in data
    productIdInvalidType = not isinstance(data["productId"], int)
    productNameInvalidType = not isinstance(data["productName"], str)
    productPictureInvalidType = not isinstance(data["productPicture"], str)
    productNameEmpty = len(data["productName"]) == 0
    
    if productIdMissing or productNameMissing or productPictureMissing or productIdInvalidType or productNameInvalidType or productPictureInvalidType or productNameEmpty:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    return data

def validateErrorMessage(data: Dict[str, Any]) -> Dict[str, Any]:
    errorMessageMissing = "errorMessage" not in data
    errorMessageInvalidType = not isinstance(data["errorMessage"], str)
    errorMessageEmpty = len(data["errorMessage"]) == 0
    if errorMessageMissing or errorMessageInvalidType or errorMessageEmpty:
            raise HTTPException(status_code=400, detail="Bad Request")
    return data