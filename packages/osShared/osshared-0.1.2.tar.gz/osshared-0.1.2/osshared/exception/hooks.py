# osShared/exception/hooks.py

from typing import Any, Dict, List, Union
from rest_framework.views import exception_handler
from rest_framework.response import Response
from osshared.response.responseBuilder import ResponseBuilder
from osshared.exception.exception import OsBaseException
import traceback


def global_exception_handler(exc: Exception, context: Dict[str, Any]) -> Response:
    """
    전역 예외 처리 핸들러

    Args:
        exc: 발생한 예외 객체
        context: 예외 발생 컨텍스트 (request, view 등)

    Returns:
        Response: 표준화된 에러 응답
    """
    # 커스텀 예외 처리
    if isinstance(exc, OsBaseException):
        return Response(
            ResponseBuilder.buildError(
                message=exc.message,
                errors=[{
                    "code": exc.code,
                    "message": exc.message,
                }]
            ),
            status=exc.status_code
        )

    # 기본 DRF 예외 핸들링으로 fallback
    response = exception_handler(exc, context)

    if response is not None:
        return Response(
            ResponseBuilder.buildError(
                message="Unhandled error occurred",
                errors=[{
                    "code": "UNHANDLED",
                    "message": str(exc),
                    "trace": traceback.format_exc()
                }]
            ),
            status=response.status_code
        )

    # 알 수 없는 에러
    return Response(
        ResponseBuilder.buildError(
            message="Internal Server Error",
            errors=[{
                "code": "INTERNAL_ERROR",
                "message": str(exc),
                "trace": traceback.format_exc()
            }]
        ),
        status=500
    )
