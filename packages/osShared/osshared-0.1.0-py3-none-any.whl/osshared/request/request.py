"""
API 요청 DTO 정의
"""

class SampleRequest:
    def __init__(self, user_id: int):
        self.user_id = user_id
