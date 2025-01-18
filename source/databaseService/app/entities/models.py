from typing import List
from pydantic import BaseModel

class Request(BaseModel):
    ids: List[int]

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