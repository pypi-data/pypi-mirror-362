import akridata_akrimanager_v2 as am

from akride._utils.catalog.dataset_tables_info import DatasetTablesInfo
from akride._utils.catalog.pipeline_tables_info import PipelineTablesInfo
from akride._utils.progress_manager.progress_step import ProgressStep
from akride._utils.video_splitter.splitter import VideoSplitter
from akride.core._filters.partitioners.ingest.ingest_image_partitioner_filter import (
    ImageIngestPartitionerFilter,
)
from akride.core._filters.partitioners.ingest.ingest_partitioner_filter import (
    IngestPartitionerFilter,
)
from akride.core._filters.partitioners.ingest.ingest_video_partitioner_filter import (
    VideoIngestPartitionerFilter,
)
from akride.core._filters.partitioners.process.image_process_partitioner_filter import (
    ImageProcessPartitionerFilter,
)
from akride.core._filters.partitioners.process.process_partitioner_filter import (
    ProcessPartitionerFilter,
)
from akride.core._filters.partitioners.process.video_process_partitioner_filter import (
    VideoProcessPartitionerFilter,
)
from akride.core.enums import DataType


class PartitionerFilterFactory:
    @staticmethod
    def get_ingest_partitioner(
        dataset: am.DataSetJSON,
        data_dir: str,
        session_id: str,
        workflow_id: str,
        dataset_tables_info: DatasetTablesInfo,
        ccs_api: am.CcsApi,
        ingest_step: ProgressStep,
        data_type: DataType,
    ) -> IngestPartitionerFilter:
        if data_type == DataType.IMAGE:
            return ImageIngestPartitionerFilter(
                dataset=dataset,
                data_dir=data_dir,
                session_id=session_id,
                workflow_id=workflow_id,
                dataset_tables_info=dataset_tables_info,
                ccs_api=ccs_api,
                ingest_step=ingest_step,
            )

        elif data_type == DataType.VIDEO:
            return VideoIngestPartitionerFilter(
                dataset=dataset,
                data_dir=data_dir,
                session_id=session_id,
                workflow_id=workflow_id,
                dataset_tables_info=dataset_tables_info,
                ccs_api=ccs_api,
                ingest_step=ingest_step,
            )

        raise ValueError(f"Unsupported dataset datatype {data_type.value}")

    @staticmethod
    def get_process_partitioner(
        dataset_id: str,
        pipeline_tables_info: PipelineTablesInfo,
        dataset_tables_info: DatasetTablesInfo,
        ccs_api: am.CcsApi,
        data_type: DataType,
        sample_frame_rate: float = -1,
    ) -> ProcessPartitionerFilter:
        if data_type == DataType.IMAGE:
            return ImageProcessPartitionerFilter(
                dataset_id=dataset_id,
                pipeline_tables_info=pipeline_tables_info,
                dataset_tables_info=dataset_tables_info,
                ccs_api=ccs_api,
            )
        elif data_type == DataType.VIDEO:
            splitter = VideoSplitter(sampling_rate=sample_frame_rate)
            return VideoProcessPartitionerFilter(
                dataset_id=dataset_id,
                pipeline_tables_info=pipeline_tables_info,
                dataset_tables_info=dataset_tables_info,
                ccs_api=ccs_api,
                video_splitter=splitter,
            )

        raise ValueError(f"Unsupported dataset datatype {data_type.value}")
