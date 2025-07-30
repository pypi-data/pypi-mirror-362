from pathlib import Path
from typing import List, Optional, Tuple

import akridata_akrimanager_v2 as am
from pyakri_de_utils.file_utils import (
    copy_files_to_dir,
    get_file_name_from_path,
)
from pyakri_de_utils.image_utils import ImageUtils

from akride._utils.catalog.dataset_tables_info import DatasetTablesInfo
from akride._utils.catalog.pipeline_tables_info import PipelineTablesInfo
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


class ImageProcessPartitionerFilter(ProcessPartitionerFilter):
    def __init__(
        self,
        dataset_id: str,
        pipeline_tables_info: PipelineTablesInfo,
        dataset_tables_info: DatasetTablesInfo,
        ccs_api: am.CcsApi,
    ):
        super().__init__(
            dataset_id=dataset_id,
            ccs_api=ccs_api,
            pipeline_tables_info=pipeline_tables_info,
            dataset_tables_info=dataset_tables_info,
            token_size=Constants.PROCESS_IMAGE_WF_TOKEN_SIZE,
        )

    def _prepare_directories(
        self, out_dirs: FilterWorkingDirectories, token: ProcessTokenInfo
    ):
        # Prepare partitioner output directory
        copy_files_to_dir(files=token.files, dst_dir=out_dirs.out_dir)

        # Prepare metadata directory
        self._prepare_metadata_dir(
            filemeta_list=token.file_meta_list,
            metadata_dir=out_dirs.metadata_dir,
        )

    def _prepare_token(
        self, token: BatchInfo, out_dirs: FilterWorkingDirectories
    ) -> List[ProcessTokenInfo]:
        file_id = token.next_file_id

        filemeta_arr_list, file_info_list = [], []
        frame_idx_in_blob, frame_idx_in_file = 0, 0

        partition_end = self._get_partition_end(token.partition_start)

        for file in token.files:
            image_dim: Optional[Tuple[int, int]] = ImageUtils.get_image_size(
                file=Path(file)
            )

            file_info_list.append(
                ProcessFileInfo(
                    file_path=file,
                    file_id=file_id,
                    frame_idx_in_blob=frame_idx_in_blob,
                    partition_start=token.partition_start,
                    partition_end=partition_end,
                    file_name=get_file_name_from_path(file),
                    frame_idx_in_file=frame_idx_in_file,
                    total_frames_in_file=1,
                    frame_width=image_dim[0],
                    frame_height=image_dim[1],
                )
            )
            filemeta_arr_list.append([file_id, file, frame_idx_in_file])
            frame_idx_in_blob += 1
            file_id += 1

        token = ProcessTokenInfo(
            file_info_list=file_info_list,
            file_meta_list=filemeta_arr_list,
            token_number=token.number,
            total_num_tokens=token.total_count,
            files=token.files,
            parent_dir=out_dirs.parent_dir,
            metadata_dir=out_dirs.metadata_dir,
            out_dir=out_dirs.out_dir,
        )

        # Prepare directories
        self._prepare_directories(out_dirs=out_dirs, token=token)

        return [token]

    def _process_token(
        self, token: BatchInfo, output_dirs: FilterWorkingDirectories
    ) -> List[ProcessTokenInfo]:
        return self._prepare_token(token=token, out_dirs=output_dirs)
