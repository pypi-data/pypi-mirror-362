from dataclasses import dataclass
from typing import Any, List, Optional

from akride.core._filters.partitioners.models import ProcessFileInfo


@dataclass
class ProcessTokenInfo:
    file_info_list: List[ProcessFileInfo]
    file_meta_list: List[List[Any]]
    files: List[str]
    token_number: int

    total_num_tokens: int

    out_dir: str
    parent_dir: str
    metadata_dir: str

    # Will be set only for video datasets
    partition_num: Optional[int] = None
    total_partitions: Optional[int] = None

    def should_update_progress(self) -> bool:
        # Will be set only for video datasets
        if self.partition_num is not None:
            return self.partition_num == self.total_partitions

        return True


@dataclass
class FilterWorkingDirectories:
    out_dir: str
    metadata_dir: str
    parent_dir: str


@dataclass
class BatchInfo:
    number: int
    files: List[str]
    partition_start: int
    next_file_id: int
    total_count: int


@dataclass
class UnProcessedFilesInfo:
    files: List[str]
