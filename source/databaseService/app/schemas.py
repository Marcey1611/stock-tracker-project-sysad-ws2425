from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StockLogCreate(BaseModel):
    product_id: int
    systemtimein: datetime
    systemtimeout: Optional[datetime] = None

class ProductCreate(BaseModel):
    product_name: str

    class Config:
        orm_mode = True

class StockLogResponse(BaseModel):
    stocklog_id: int
    product_id: int
    systemtimein: datetime
    systemtimeout: Optional[datetime]

    class Config:
        orm_mode = True
