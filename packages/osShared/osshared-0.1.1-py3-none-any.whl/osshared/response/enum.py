"""
Response Enum 정의
"""
from enum import Enum

class enumResponseStatus(str, Enum):
    OK = "ok"
    ERROR = "error"
