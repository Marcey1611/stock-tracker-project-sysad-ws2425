from enum import Enum

class httpStatusCode(Enum):
    OK = 200
    BAD_REQUEST = 400
    CONFLICT = 409
    SERVER_ERROR = 500