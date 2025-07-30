import math
import threading
from abc import abstractmethod
from typing import Any, List, Optional

import akridata_akrimanager_v2 as am
import pandas as pd
from pyakri_de_utils.arrow_utils import write_arrow_from_df
from pyakri_de_utils.file_utils import (
    concat_file_paths,
    create_directories,
    create_directory,
    create_temp_directory,
    get_filter_output_dir,
    remove_directory,
)

from akride import Constants, logger
from akride._utils.catalog.dataset_tables_info import DatasetTablesInfo
from akride._utils.catalog.pipeline_tables_info import PipelineTablesInfo
from akride.core._filters.partitioners.dtos import (
    BatchInfo,
    FilterWorkingDirectories,
    ProcessTokenInfo,
    UnProcessedFilesInfo,
)
from akride.core._filters.partitioners.partitioner_filter import (
    PartitionerFilter,
)


class ProcessPartitionerFilter(PartitionerFilter):
    DF_COLUMNS = ["file_id", "filename", "frame_idx_in_file"]
    DEST_ARROW_FILE = "0-1"

    PARTITION_TIME_FRAME = Constants.PARTITION_TIME_FRAME

    def __init__(
        self,
        dataset_id: str,
        ccs_api: am.CcsApi,
        pipeline_tables_info: PipelineTablesInfo,
        dataset_tables_info: DatasetTablesInfo,
        token_size: int,
        partition_size: Optional[int] = None,
    ):
        super().__init__(
            dataset_id=dataset_id,
            ccs_api=ccs_api,
            partition_size=partition_size,
            token_size=token_size,
        )

        self._pipeline_tables_info = pipeline_tables_info
        self._dataset_tables_info = dataset_tables_info

        self._tmp_dirs_map = {}

        self._lock = threading.Lock()

        self._tmp_dir_base_path = Constants.AKRIDE_TMP_DIR

    @staticmethod
    def _get_output_dirs(
        parent_directory: str, filter_directory: str, token_num: int
    ) -> FilterWorkingDirectories:
        token_num_str = str(token_num)

        output_dir = concat_file_paths(filter_directory, token_num_str, "o1")
        metadata_dir = concat_file_paths(
            filter_directory, "metadata", token_num_str, "o1"
        )

        return FilterWorkingDirectories(
            parent_dir=parent_directory,
            out_dir=output_dir,
            metadata_dir=metadata_dir,
        )

    @classmethod
    def _prepare_metadata_dir(
        cls, metadata_dir: str, filemeta_list: List[List[Any]]
    ):
        data_frame_to_write = pd.DataFrame(
            filemeta_list, columns=cls.DF_COLUMNS
        )
        create_directory(metadata_dir)

        dst_arrow_file_path = concat_file_paths(
            metadata_dir, cls.DEST_ARROW_FILE
        )

        write_arrow_from_df(data_frame_to_write, dst_arrow_file_path)

    def _get_next_file_id(self, primary_table_name: str) -> int:
        response: am.CCSFetchMaxFileIdPartitionIdResponse = (
            self._ccs_api.fetch_max_fileid_partitionid(
                dataset_id=self._dataset_id,
                abs_table_name=primary_table_name,
                is_fetch_max_partition=False,
            )
        )
        max_file_id = response.max_file_id
        next_file_id = 0 if max_file_id is None else max_file_id + 1
        return next_file_id

    def _get_partition_end(self, start: int) -> int:
        return start + self.PARTITION_TIME_FRAME - 1

    def _register_sub_token_directories(
        self, token_info: List[ProcessTokenInfo]
    ):
        with self._lock:
            for token in token_info:
                if token.partition_num is not None:
                    self._tmp_dirs_map[
                        (token.token_number, token.partition_num)
                    ] = token.parent_dir

    def _get_temporary_working_directory(self, token_num: int) -> str:
        if token_num in self._tmp_dirs_map:
            return self._tmp_dirs_map[token_num]

        create_directory(self._tmp_dir_base_path)

        out_dir = create_temp_directory(dir_path=self._tmp_dir_base_path)

        # Update tmp dirs map
        with self._lock:
            self._tmp_dirs_map[token_num] = out_dir.name

        return out_dir.name

    def _get_filter_working_directories(
        self, token_number: int
    ) -> FilterWorkingDirectories:
        working_dir = self._get_temporary_working_directory(
            token_num=token_number
        )

        filter_directory = get_filter_output_dir(
            par_dir=working_dir, filter_type=self._filter_type.value
        )

        out_dirs: FilterWorkingDirectories = self._get_output_dirs(
            parent_directory=working_dir,
            filter_directory=filter_directory,
            token_num=token_number,
        )

        create_directories([out_dirs.out_dir, out_dirs.metadata_dir])

        return out_dirs

    def run(self):
        partitioned_table_name = (
            self._dataset_tables_info.get_partitioned_abs_table()
        )
        primary_table_name = self._pipeline_tables_info.get_primary_abs_table()

        next_file_id = self._get_next_file_id(primary_table_name)

        # Get total number of tokens to process
        total_file_count = self._get_total_file_count(
            primary_table_name=primary_table_name,
            partitioned_table_name=partitioned_table_name,
        )
        token_count = math.ceil(total_file_count / self._token_size)
        logger.debug(
            f"There are {token_count} tokens to be "
            f"processed for pipeline {self._pipeline_tables_info.get_pipeline_name()}"
        )

        # Yield token
        partition_start = 0
        token_index = 0

        while token_index < token_count:
            token_number = token_index + 1

            logger.debug(
                f"Getting unprocessed files for token {token_index} count {token_count}"
            )

            # Fetch unprocessed token
            unprocessed_files: UnProcessedFilesInfo = (
                self._get_unprocessed_files(
                    primary_table_name=primary_table_name,
                    partitioned_table_name=partitioned_table_name,
                )
            )

            logger.debug(
                f"Got unprocessed files for token {token_index} count {token_count}"
            )

            # Process and yield files to be processed
            batch_token = BatchInfo(
                files=unprocessed_files.files,
                partition_start=partition_start,
                number=token_number,
                next_file_id=next_file_id,
                total_count=token_count,
            )

            output_dirs = self._get_filter_working_directories(
                token_number=batch_token.number
            )

            processed_tokens: List[ProcessTokenInfo] = self._process_token(
                token=batch_token, output_dirs=output_dirs
            )

            # Register sub token directories
            self._register_sub_token_directories(processed_tokens)

            for token in processed_tokens:
                yield token

            # Update counters
            partition_start += (
                len(processed_tokens) * self.PARTITION_TIME_FRAME
            )
            next_file_id += self._token_size

            token_index += 1

    def cleanup_token(self, token_num, partition_num: Optional[int] = None):
        logger.debug(
            f"Cleaning temporary directories for token {token_num}, "
            f"sub_token {partition_num}"
        )
        if partition_num:
            key = (token_num, partition_num)
        else:
            key = token_num

        tmp_dir = self._tmp_dirs_map.get(key)

        if tmp_dir:
            remove_directory(directory=tmp_dir)

            with self._lock:
                self._tmp_dirs_map.pop(key)

        logger.debug(f"Cleaned temporary directories for token {key}")

    def cleanup(self):
        logger.debug("Cleaning temporary directories!")

        for _, tmp_dir in self._tmp_dirs_map.items():
            remove_directory(directory=tmp_dir)

        logger.debug("Cleaned temporary directories!")

    def _get_total_file_count(
        self, primary_table_name: str, partitioned_table_name: str
    ) -> int:
        response: am.CCSFetchUnprocessedFileCntResponse = (
            self._ccs_api.fetch_unprocessed_file_count(
                dataset_id=self._dataset_id,
                primary_table=primary_table_name,
                partition_table=partitioned_table_name,
            )
        )
        return response.file_count

    def _get_unprocessed_files(
        self, primary_table_name: str, partitioned_table_name: str
    ) -> UnProcessedFilesInfo:
        response: am.CCSFetchUnprocessedFileNamesResponse = (
            self._ccs_api.fetch_unprocessed_file_names(
                dataset_id=self._dataset_id,
                primary_table=primary_table_name,
                partition_table=partitioned_table_name,
                batch_size=self._token_size,
            )
        )
        return UnProcessedFilesInfo(files=response.file_names)

    @abstractmethod
    def _process_token(
        self, token: BatchInfo, output_dirs: FilterWorkingDirectories
    ) -> List[ProcessTokenInfo]:
        pass
