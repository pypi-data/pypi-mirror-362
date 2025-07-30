from typing import Optional


class VQueueError(Exception):
    """Virtual Queue SDK exception"""


class VQueueApiError(VQueueError):
    """Exception for API responses with error status"""

    def __init__(
        self,
        code: int,
        message: Optional[str],
        error_code: Optional[int],
        data: Optional[object],
        *args,
    ):
        super().__init__(*args)
        self.code = code
        self.message = message
        self.error_code = error_code
        self.data = data

    def __str__(self) -> str:
        return f"VQueue API Error ({self.code}): {self.message or ''}"


class VQueueNetworkError(VQueueError):
    """Exception related to networking errors"""
