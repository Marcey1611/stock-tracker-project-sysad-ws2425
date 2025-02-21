from pydantic import BaseModel

class MailUpdateData(BaseModel):
    id: int
    name: str
    changed_amount: int
    amount: int

class MailErrorData(BaseModel):
    error_message: str