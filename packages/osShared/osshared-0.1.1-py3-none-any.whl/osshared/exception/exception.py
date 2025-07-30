"""
공통 예외 클래스 정의
"""

class OsBaseException(Exception):
    def __init__(self, message: str, code: str = "UNKNOWN_ERROR", status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)

class OsValidationException(OsBaseException):
    def __init__(self, message: str = "Validation Failed", code: str = "VALIDATION_ERROR"):
        super().__init__(message=message, code=code, status_code=422)

class OsNotFoundException(OsBaseException):
    def __init__(self, message: str = "Resource Not Found", code: str = "NOT_FOUND"):
        super().__init__(message=message, code=code, status_code=404)
