from dataclasses import dataclass
from datetime import datetime

import akridata_akrimanager_v2 as am


@dataclass
class BGCAttachmentJobStatus:
    job_id: str

    status: am.BCJobStatus
    error_logs: str
    progress: float

    start_time: datetime
    end_time: datetime
