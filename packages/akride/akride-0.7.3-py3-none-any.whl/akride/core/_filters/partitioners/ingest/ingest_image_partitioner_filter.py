import akridata_akrimanager_v2 as am

from akride import Constants
from akride._utils.catalog.dataset_tables_info import DatasetTablesInfo
from akride._utils.progress_manager.progress_step import ProgressStep
from akride.core._filters.partitioners.ingest.ingest_partitioner_filter import (
    IngestPartitionerFilter,
)


class ImageIngestPartitionerFilter(IngestPartitionerFilter):
    def __init__(
        self,
        dataset: am.DataSetJSON,
        data_dir: str,
        session_id: str,
        workflow_id: str,
        dataset_tables_info: DatasetTablesInfo,
        ccs_api: am.CcsApi,
        ingest_step: ProgressStep,
    ):
        super().__init__(
            dataset=dataset,
            data_dir=data_dir,
            session_id=session_id,
            workflow_id=workflow_id,
            dataset_tables_info=dataset_tables_info,
            ccs_api=ccs_api,
            ingest_step=ingest_step,
            partition_size=Constants.INGEST_IMAGE_PARTITION_SIZE,
            token_size=Constants.INGEST_IMAGE_WF_TOKEN_SIZE,
        )
