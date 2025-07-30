from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ImportCatalogJobOut:
    job_id: str


@dataclass
class ImportCatalogJobDetails:
    job_id: str
    status: str
    started_at: datetime
    completed_at: datetime
    error: Optional[str] = None
