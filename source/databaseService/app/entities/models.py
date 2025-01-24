from typing import List, Dict
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    total_amount: int
    picture: str | None = None

class Request(BaseModel):
    products = Dict[int, Product]
    overall_picture: str

class Response(BaseModel):
    status_code: int

class MailResponse(BaseModel):
    product_id: int
    product_name: str
    product_amount_total: int
    product_amount_changed: int
    error_message: str | None = None

class AppResponse(BaseModel):
    products = Dict[int, Product]
    overall_picture: str