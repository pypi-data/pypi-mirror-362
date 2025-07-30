"""
Response Builder 정의
"""
from typing import Any, Optional
from datetime import datetime
from osShared.response.enum import enumResponseStatus
from osShared.response.response import ResponseBase

import uuid

class ResponseBuilder:
    @staticmethod
    def buildOk(
        data: Optional[Any] = None,
        message: Optional[str] = "backend.common.ok",
        traceid: Optional[str] = None,
    ) -> ResponseBase:
        return ResponseBase(
            status=enumResponseStatus.OK,
            message=message,
            data=data,
            traceid=traceid or str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
        )

    @staticmethod
    def buildError(
        message: Optional[str] = "backend.common.error",
        errors: Optional[Any] = None,
        traceid: Optional[str] = None,
    ) -> ResponseBase:
        return ResponseBase(
            status=enumResponseStatus.ERROR,
            message=message,
            errors=errors,
            traceid=traceid or str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
        )
