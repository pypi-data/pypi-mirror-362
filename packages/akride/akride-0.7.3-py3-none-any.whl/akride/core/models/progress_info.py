from dataclasses import dataclass
from typing import Optional


# Class representing progress information for an operation.
@dataclass
class ProgressInfo:
    percent_completed: float
    message: Optional[str] = None
    completed: bool = False
    error: str = None
    failed: bool = False
