from typing import Dict, List

import akridata_akrimanager_v2 as am
from pyakri_de_utils.file_utils import get_file_name_from_path

from akride import logger
from akride._utils.catalog.dataset_tables_info import DatasetTablesInfo
from akride._utils.catalog.pipeline_tables_info import PipelineTablesInfo
from akride._utils.video_splitter.models import VideoSplitOut
from akride._utils.video_splitter.splitter import VideoSplitter
from akride.core._filters.partitioners.dtos import (
    BatchInfo,
    FilterWorkingDirectories,
    ProcessTokenInfo,
)
from akride.core._filters.partitioners.models import ProcessFileInfo
from akride.core._filters.partitioners.process.process_partitioner_filter import (
    ProcessPartitionerFilter,
)
from akride.core.constants import Constants


class VideoProcessPartitionerFilter(ProcessPartitionerFilter):
    def __init__(
        self,
        dataset_id: str,
        pipeline_tables_info: PipelineTablesInfo,
        dataset_tables_info: DatasetTablesInfo,
        ccs_api: am.CcsApi,
        video_splitter: VideoSplitter,
    ):
        super().__init__(
            dataset_id=dataset_id,
            ccs_api=ccs_api,
            pipeline_tables_info=pipeline_tables_info,
            dataset_tables_info=dataset_tables_info,
            token_size=Constants.PROCESS_VIDEO_WF_TOKEN_SIZE,
        )

        self._video_splitter = video_splitter

    def _split_video_to_frames(
        self, file: str, out_dir: str, token_num: int
    ) -> Dict[str, VideoSplitOut]:
        frames_map = {}
        try:
            video_split_info: VideoSplitOut = self._video_splitter.split(
                file=file, out_dir=out_dir, token_num=token_num
            )

            return {file: video_split_info}
        except Exception as ex:
            logger.debug(f"Failed to split video {file} with exception {ex}")
            return frames_map

    def _prepare_tokens(
        self,
        token: BatchInfo,
        video_frames_map: Dict[str, VideoSplitOut],
    ) -> List[ProcessTokenInfo]:
        process_tokens = []

        file_id = token.next_file_id

        partition_start = token.partition_start
        partition_end = self._get_partition_end(partition_start)

        for file, video_split_out in video_frames_map.items():
            file_name = get_file_name_from_path(file)

            total_frames = video_split_out.total_frames
            width = video_split_out.props.width
            height = video_split_out.props.height
            fps = video_split_out.props.fps

            total_partitions = len(video_split_out.partitions)

            for partition in video_split_out.partitions:
                frame_idx_in_blob = 0

                filemeta_arr_list, file_info_list = [], []

                for frame_info in partition.frames:
                    file_info_list.append(
                        ProcessFileInfo(
                            file_path=file,
                            file_id=file_id,
                            frame_idx_in_blob=frame_idx_in_blob,
                            partition_start=partition_start,
                            partition_end=partition_end,
                            file_name=file_name,
                            frame_idx_in_file=frame_info.index,
                            total_frames_in_file=total_frames,
                            frame_width=width,
                            frame_height=height,
                            native_fps=fps,
                        )
                    )
                    filemeta_arr_list.append([file_id, file, frame_info.index])

                    frame_idx_in_blob += 1

                process_token = ProcessTokenInfo(
                    file_info_list=file_info_list,
                    file_meta_list=filemeta_arr_list,
                    token_number=token.number,
                    total_num_tokens=token.total_count,
                    files=token.files,
                    metadata_dir=partition.metadata_dir,
                    parent_dir=partition.parent_dir,
                    partition_num=partition.num,
                    out_dir=partition.out_dir,
                    total_partitions=total_partitions,
                )

                process_tokens.append(process_token)

                partition_start = partition_end + 1
                partition_end = self._get_partition_end(start=partition_start)

            file_id += 1

        # Prepare directories
        for token in process_tokens:
            self._prepare_metadata_dir(
                metadata_dir=token.metadata_dir,
                filemeta_list=token.file_meta_list,
            )

        return process_tokens

    def _process_token(
        self, token: BatchInfo, output_dirs: FilterWorkingDirectories
    ) -> List[ProcessTokenInfo]:
        # Only 1 video file per token is supported
        video_frames_map: Dict[
            str, VideoSplitOut
        ] = self._split_video_to_frames(
            file=token.files[0],
            out_dir=output_dirs.out_dir,
            token_num=token.number,
        )

        return self._prepare_tokens(
            token=token,
            video_frames_map=video_frames_map,
        )
