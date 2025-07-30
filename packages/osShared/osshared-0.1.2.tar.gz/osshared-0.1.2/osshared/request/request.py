"""
API Request DTO 정의
"""
from typing import Generic, TypeVar, Optional
from osshared.request.enum import enumActionType
from pydantic import BaseModel


class SampleRequest:
    def __init__(self, user_id: int):
        self.user_id = user_id


T = TypeVar('T')
class RequestBase(Generic[T], BaseModel):
    action: enumActionType
    payload: T
    traceid: Optional[str] = None
