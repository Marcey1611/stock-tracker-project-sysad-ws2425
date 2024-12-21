from typing import List
from pydantic import BaseModel

class Request(BaseModel):
    ids: List[int]

class Response(BaseModel):
    statusCode: int

class MailResponse(BaseModel):
    productID: int
    productName: str
    productPicture: str
    productAmountTotal: int
    productAmountAdded: int
    errorMessage: str | None = None