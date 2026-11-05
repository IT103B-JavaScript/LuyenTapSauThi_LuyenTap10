"""
Ngoại lệ nghiệp vụ dùng chung: service ném ra, main.py bắt và trả về đúng cấu trúc response chung.
"""


class AppException(Exception):
    def __init__(self, status_code: int, error: str, message: str):
        self.status_code = status_code
        self.error = error
        self.message = message
        super().__init__(message)
