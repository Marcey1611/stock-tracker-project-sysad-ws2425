from typing import List, Dict
from pydantic import BaseModel

class Request(BaseModel):
    products: List[int]
    pictures: Dict[int, str]
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
    product_id: int
    product_name: str
    product_picture: str | None = None
    product_amount: int