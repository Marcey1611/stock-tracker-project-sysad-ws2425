from fastapi import HTTPException

class InternalErrorException(HTTPException):
    def __init__(self, detail: str = "Internal Server Error", status_code: int = 500):
        super().__init__(status_code=status_code, detail=detail)