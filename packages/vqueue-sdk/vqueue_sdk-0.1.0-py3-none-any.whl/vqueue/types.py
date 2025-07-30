from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class VerificationResultData:
    token: str
    ingressed_at: datetime
    finished_at: datetime


@dataclass
class VerificationResult:
    message: str
    success: bool
    data: Optional[VerificationResultData] = None
