from typing import NamedTuple, Optional


class ProcessFileInfo(NamedTuple):
    partition_start: int
    partition_end: int
    file_id: int
    file_path: str
    file_name: str
    frame_height: int
    frame_width: int

    frame_idx_in_blob: int
    frame_idx_in_file: int
    total_frames_in_file: int

    blob_idx_in_partition: int = 0

    native_fps: Optional[float] = None
