"""
API Response DTO 정의
"""
from typing import Generic, TypeVar, Optional, Any
from osshared.response.enum import enumResponseStatus
from pydantic import BaseModel
from datetime import datetime

class SampleResponse:
    def __init__(self, message: str):
        self.message = message


T = TypeVar('T')
class ResponseBase(Generic[T], BaseModel):
    status: enumResponseStatus
    message: Optional[str] = None
    data: Optional[T] = None
    error: Optional[Any] = None
    traceid: Optional[str] = None
    timestamp: str = datetime.now().isoformat()
