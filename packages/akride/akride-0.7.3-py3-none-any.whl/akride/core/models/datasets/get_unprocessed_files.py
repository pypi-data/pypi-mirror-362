from dataclasses import dataclass
from typing import List


@dataclass
class DatasetUnprocessedFiles:
    file_paths: List[str]
