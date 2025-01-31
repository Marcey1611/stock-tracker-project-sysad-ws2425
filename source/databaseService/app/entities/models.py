from typing import Dict
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    amount: int
    picture: str | None = None

class Request(BaseModel):
    products = Dict[int, Product]
    overall_picture: str

class Response(BaseModel):
    status_code: int

class MailResponse(BaseModel):
    id: int
    name: str
    amount: int
    changed_amount: int
    error_message: str | None = None

class AppResponse(BaseModel):
    products = Dict[int, Product]
    overall_picture: str