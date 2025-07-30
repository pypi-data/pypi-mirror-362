import re
from pathlib import Path
from typing import List

from pyakri_de_utils.file_utils import (
    concat_file_paths,
    create_directories,
    get_input_files_batch,
    get_json_from_file,
    get_sorted_dirs_from_path,
)

from akride import Constants, logger
from akride._utils.common_utils import get_random_uuid
from akride._utils.resource_utils import get_video_splitter_script
from akride._utils.shell_utils import run_subprocess
from akride._utils.video_splitter.models import (
    FrameInfo,
    SplitterDirs,
    VideoProps,
    VideoSplitOut,
    VideoSplitterPartition,
)
from akride.core._filters.enums import FilterTypes
from akride.core.exceptions import ServerError


class VideoSplitter:
    METADATA_FILE = ".METADATA.txt"

    OUTPUT_PREFIX = concat_file_paths(
        FilterTypes.Partitioner.value, "outputs", "o1"
    )

    METADATA_DIR = "metadata"

    SPLIT_VIDEO_SCRIPT = get_video_splitter_script("split_video.sh")

    def __init__(
        self,
        sampling_rate: float,
        output_format: str = "jpg",
        output_file_name: str = "frame",
        chunk_size: int = Constants.VIDEO_CHUNK_SIZE,
        output_parent_dir: str = Constants.AKRIDE_TMP_DIR,
    ):
        self._output_format = output_format
        self._output_file_name = output_file_name
        self._sampling_rate = sampling_rate
        self._chunk_size = chunk_size

        self._output_parent_dir = output_parent_dir

    def _get_output_dir_for_splitter(self, token_num: int):
        return concat_file_paths(
            self._output_parent_dir, get_random_uuid(), str(token_num)
        )

    def _get_dirs(
        self, file: str, out_dir: str, token_num: int
    ) -> SplitterDirs:
        metadata_dir = concat_file_paths(out_dir, self.METADATA_DIR)
        metadata_file = concat_file_paths(metadata_dir, self.METADATA_FILE)

        output_parent_dir = self._get_output_dir_for_splitter(
            token_num=token_num
        )

        create_directories([output_parent_dir, metadata_dir])

        return SplitterDirs(
            input_file=file,
            out_parent_dir=output_parent_dir,
            metadata_file=metadata_file,
        )

    @staticmethod
    def _get_file_index(file_path: Path):
        # Input string
        filename = file_path.name

        # Search for the pattern in the input string
        matches = re.findall(r"\d{7}", filename)
        if matches:
            return int(matches[0]) - 1

        raise ValueError("Failed to get frame index")

    @classmethod
    def _get_video_partitions(
        cls,
        parent_dir: str,
    ) -> (List[VideoSplitterPartition], int):
        partitions: List[VideoSplitterPartition] = []
        total_frames = 0

        partition_dirs = get_sorted_dirs_from_path(path=parent_dir)

        # Iterate through each item in the parent directory
        for partition_num, subdir in enumerate(partition_dirs):
            partition_dir = concat_file_paths(parent_dir, subdir)

            output_dir = concat_file_paths(partition_dir, cls.OUTPUT_PREFIX)
            metadata_dir = concat_file_paths(partition_dir, cls.METADATA_DIR)

            file_paths = next(
                get_input_files_batch(
                    directory=partition_dir, extension=".jpg"
                )
            )

            frames = []
            for file_path in file_paths:
                frames.append(
                    FrameInfo(
                        index=cls._get_file_index(file_path), file=file_path
                    )
                )

            if frames:
                partitions.append(
                    VideoSplitterPartition(
                        num=partition_num + 1,
                        out_dir=output_dir,
                        metadata_dir=metadata_dir,
                        parent_dir=partition_dir,
                        frames=frames,
                    )
                )
                total_frames += len(file_paths)

        return partitions, total_frames

    def _get_video_metadata(self, metadata_file: str) -> VideoProps:
        metadata = get_json_from_file(file=metadata_file)

        return VideoProps(
            width=metadata["width"],
            height=metadata["height"],
            fps=metadata["fps"],
            duration=metadata["duration"],
        )

    def split(self, file: str, out_dir: str, token_num: int) -> VideoSplitOut:
        directories: SplitterDirs = self._get_dirs(
            file=file, out_dir=out_dir, token_num=token_num
        )

        script_args = [
            self._chunk_size,
            self._sampling_rate,
            directories.input_file,
            directories.out_parent_dir,
            directories.metadata_file,
            out_dir,
        ]

        result = run_subprocess(self.SPLIT_VIDEO_SCRIPT, *script_args)

        # Raise exception if video splitter failed
        if result.has_failed():
            raise ServerError(
                f"Failed to split video with error {result.stderr}"
            )

        # Read metadata
        video_metadata: VideoProps = self._get_video_metadata(
            directories.metadata_file
        )

        # Get partitions
        partitions, total_frames = self._get_video_partitions(
            parent_dir=directories.out_parent_dir
        )

        logger.debug(f"Num partitions are {len(partitions)}")

        return VideoSplitOut(
            props=video_metadata,
            total_frames=total_frames,
            partitions=partitions,
        )
