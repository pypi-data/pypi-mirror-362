"""
공통 예외 클래스 정의 (예: 인증 실패, 권한 없음 등)
"""

class AuthError(Exception):
    def __init__(self, message: str):
        super().__init__(f"[AuthError] {message}")
