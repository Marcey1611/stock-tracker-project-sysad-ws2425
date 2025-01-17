from typing import List, Dict
from pydantic import BaseModel

class Request(BaseModel):
    products: List[int]
    pictures: Dict[int: str]
    overall_picture: str

class Response(BaseModel):
    statusCode: int

class MailResponse(BaseModel):
    productId: int
    productName: str
    productAmountTotal: int
    productAmountAdded: int
    errorMessage: str | None = None

class AppResponse(BaseModel):
    productId: int
    productName: str
    productPicture: str | None = None
    productAmount: int