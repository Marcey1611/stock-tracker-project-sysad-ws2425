from typing import Dict
from pydantic import BaseModel

from entities.detection.product import Product


class DatabaseUpdateRequest(BaseModel):
    products: Dict[int, Product]
    overall_picture: str


class DatabaseUpdateResponse(BaseModel):
    status_code: int
