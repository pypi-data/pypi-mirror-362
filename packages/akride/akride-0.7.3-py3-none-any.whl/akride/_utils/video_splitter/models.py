from dataclasses import dataclass
from typing import List


@dataclass
class SplitterDirs:
    input_file: str
    out_parent_dir: str
    metadata_file: str


@dataclass
class FrameInfo:
    index: int
    file: str


@dataclass
class VideoSplitterPartition:
    num: int

    frames: List[FrameInfo]

    parent_dir: str
    out_dir: str
    metadata_dir: str


@dataclass
class VideoProps:
    width: int
    height: int
    fps: float
    duration: float


@dataclass
class VideoSplitOut:
    props: VideoProps

    partitions: List[VideoSplitterPartition]

    total_frames: int
