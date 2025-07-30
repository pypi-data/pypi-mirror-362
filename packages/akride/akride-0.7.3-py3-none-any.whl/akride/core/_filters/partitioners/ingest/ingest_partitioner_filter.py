import math
from pathlib import Path
from typing import List, Tuple

import akridata_akrimanager_v2 as am
from pyakri_de_utils.file_utils import (
    get_files_in_batches,
    get_input_files_batch,
)

from akride import logger
from akride._utils.catalog.dataset_tables_info import DatasetTablesInfo
from akride._utils.catalog.enums import TableNames
from akride._utils.progress_manager.manager import ProgressStep
from akride.core._filters.partitioners.partitioner_filter import (
    PartitionerFilter,
)
from akride.core.constants import Constants


class IngestPartitionerFilter(PartitionerFilter):
    def __init__(
        self,
        dataset: am.DataSetJSON,
        data_dir: str,
        session_id: str,
        workflow_id: str,
        dataset_tables_info: DatasetTablesInfo,
        ccs_api: am.CcsApi,
        ingest_step: ProgressStep,
        partition_size: int,
        token_size: int,
    ):
        super().__init__(
            dataset_id=dataset.id,
            ccs_api=ccs_api,
            partition_size=partition_size,
            token_size=token_size,
        )

        self._data_dir = data_dir
        self._dataset = dataset
        self._dataset_tables_info = dataset_tables_info
        self._session_id = session_id
        self._workflow_id = workflow_id
        self._ingest_step_progress = ingest_step

    def get_total_partitions(self, new_files: List) -> int:
        return math.ceil(len(new_files) / self._partition_size)

    def run(self):
        new_files = []
        partition_start = 0

        (
            next_file_id,
            next_partition_id,
        ) = self._get_next_file_id_and_partition_id()

        glob_pattern = self._dataset.dataset_spec.glob
        glob_pattern = (
            glob_pattern.replace("*", ".*") if glob_pattern else None
        )

        files_generator = get_input_files_batch(
            directory=self._data_dir,
            batch_size=self._token_size,
            glob_pattern=glob_pattern,
        )
        for files in files_generator:
            new_files += self._get_new_files(files)

        logger.debug(f"Files to be ingested: {len(new_files)}")

        total_partitions = self.get_total_partitions(new_files)

        self._ingest_step_progress.set_total_steps(total=total_partitions)

        for partition_batch in get_files_in_batches(
            file_list=new_files,
            batch_size=self._partition_size,
        ):
            for token_batch in get_files_in_batches(
                file_list=partition_batch,
                batch_size=self._token_size,
            ):
                logger.debug(
                    f"Ingesting data for token size: {len(token_batch)}"
                )
                partition_end = partition_start + self.PARTITION_TIME_FRAME - 1
                self._ingest_data_to_dataset_tables(
                    token_batch,
                    partition_start,
                    partition_end,
                    next_file_id,
                    next_partition_id,
                )
                next_file_id += self._token_size

            partition_start += self.PARTITION_TIME_FRAME

            next_partition_id += 1
            self._ingest_step_progress.increment_processed_steps(1)

    def _ingest_data_to_dataset_tables(
        self,
        files: List[str],
        partition_start: int,
        partition_end: int,
        file_id: int,
        partition_id: int,
    ):
        dataset_table_insert_values_list: List[List[str]] = []
        partitioned_table_insert_values_list: List[List[str]] = []

        for file_path in files:
            dataset_table_insert_values_list.append(
                [
                    partition_start,
                    partition_end,
                    self._workflow_id,
                    self._session_id,
                    file_path,
                ]
            )

            partitioned_table_insert_values_list.append(
                [
                    partition_start,
                    partition_end,
                    self._workflow_id,
                    self._session_id,
                    file_path,
                    file_id,
                    partition_id,
                ]
            )
            file_id += 1

        # Insert entries in dataset tables
        for table_name, columns, values in [
            (
                TableNames.DATASET_FILES.value,
                Constants.DATASET_FILES_COLUMNS,
                dataset_table_insert_values_list,
            ),
            (
                TableNames.PARTITIONER_FILES.value,
                Constants.PARTITIONED_TABLE_COLUMNS,
                partitioned_table_insert_values_list,
            ),
        ]:
            self._ccs_api.insert_data_in_catalog_table(
                insert_catalog_data=am.InsertCatalogData(
                    dataset_id=self._dataset.id,
                    table_name=table_name,
                    values=values,
                    columns=columns,
                )
            )

    def _get_next_file_id_and_partition_id(self) -> Tuple:
        response: am.CCSFetchMaxFileIdPartitionIdResponse = (
            self._ccs_api.fetch_max_fileid_partitionid(
                dataset_id=self._dataset_id,
                abs_table_name=(
                    self._dataset_tables_info.get_partitioned_abs_table()
                ),
                is_fetch_max_partition=True,
            )
        )
        max_file_id = response.max_file_id
        max_partition_id = response.max_partition_id

        next_file_id = 0 if max_file_id is None else max_file_id + 1
        next_partition_id = (
            0 if max_partition_id is None else max_partition_id + 1
        )

        return next_file_id, next_partition_id

    def _get_new_files(self, filepath_objs: List[Path]) -> List[str]:
        file_paths = [str(filepath) for filepath in filepath_objs]
        checkpointing_response: am.RegisterCheckpointingResponse = (
            self._ccs_api.register_checkpointing_query(
                am.RegisterCheckpointingRequest(
                    dataset_id=self._dataset.id,
                    file_paths=file_paths,
                )
            )
        )
        new_files = []
        for index, file_path in enumerate(file_paths):
            if checkpointing_response.is_file_path_unprocessed[index]:
                new_files.append(file_path)

        return new_files

    def cleanup(self):
        pass

    def cleanup_token(self, token_num: int):
        pass
