from enum import Enum

class Status(Enum):
    OK = "200 OK"
    BAD_REQUEST = "400 Bad Request"
    INTERNAL_SERVER_ERROR = "500 Internal Server Error"