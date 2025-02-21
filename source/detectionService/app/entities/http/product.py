from pydantic import BaseModel


class Product(BaseModel):
    name: str
    amount: int
    picture: str | None = None
