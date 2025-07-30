"""
Request Enum 정의
"""
from enum import Enum

class enumActionType(str, Enum):
    INSERT = 'insert'
    SELECT = 'select'
    UPDATE = 'update'
    DELETE = 'delete'
