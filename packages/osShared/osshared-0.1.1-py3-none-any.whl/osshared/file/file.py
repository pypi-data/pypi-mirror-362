"""
파일 관련 유틸리티 (예: 파일명 생성, 확장자 체크 등)
"""

def is_valid_extension(filename: str) -> bool:
    return filename.endswith(".json")
