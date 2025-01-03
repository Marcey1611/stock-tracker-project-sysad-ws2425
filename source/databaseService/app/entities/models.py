from typing import List
from pydantic import BaseModel

class Request(BaseModel):
    ids: List[int]

class Response(BaseModel):
    statusCode: int

class MailResponse(BaseModel):
    productId: int
    productName: str
    productPicture: str
    productAmountTotal: int
    productAmountAdded: int
    errorMessage: str | None = None

class AppResponse(BaseModel):
    products: dict