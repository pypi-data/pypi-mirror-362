import tempfile
from typing import List, Optional

import akridata_akrimanager_v2 as am
import akridata_dsp as dsp
from data_ingest_filters.data_ingest_filter_wrapper import DataIngestWrapper
from pyakri_de_utils.file_utils import concat_file_paths, get_filter_output_dir
from sink_writer_filters.enums import DataType as SinkDataType
from sink_writer_filters.models import (
    ApiManager,
    DataIngestOutputPath,
    FileInfo,
    SinkTablesInfo,
    SinkWriterFilterInput,
)
from sink_writer_filters.sink_writer_factory import SinkWriterFilterFactory

from akride import logger
from akride._utils.catalog.catalog_tables_helper import CatalogTablesHelper
from akride._utils.catalog.pipeline_tables_info import PipelineTablesInfo
from akride._utils.class_executor import ClassExecutor
from akride._utils.dataset_utils import get_dataset_type
from akride._utils.platform import is_windows_os
from akride._utils.progress_manager.manager import (
    ProgressManager,
    ProgressStep,
)
from akride._utils.workflow_helper import WorkflowHelper
from akride.core._filters.enums import FilterTypes
from akride.core._filters.partitioners.dtos import ProcessTokenInfo
from akride.core._filters.partitioners.models import ProcessFileInfo
from akride.core._filters.partitioners.partitioner_filter_factory import (
    PartitionerFilterFactory,
)
from akride.core.constants import Constants
from akride.core.enums import DataType
from akride.core.exceptions import ServerError


class PipelineExecutor:
    INGEST_WORKFLOW_PROGRESS_WEIGHTAGE = 1
    PROCESS_WORKFLOW_PROGRESS_WEIGHTAGE = 3

    """Class to run ingest and process workflow."""

    def __init__(
        self,
        dataset: am.DataSetJSON,
        data_dir: str,
        catalog_tables_helper: CatalogTablesHelper,
        pipeline_filters_info_list: List[am.AkriSDKWorkflowResponse],
        workflow_api: am.WorkflowsApi,
        dsp_dataset_api: dsp.DatasetApi,
        ccs_api: am.CcsApi,
        progress_manager: ProgressManager,
    ):
        self._dataset = dataset
        self._data_dir = data_dir
        self._catalog_tables_helper = catalog_tables_helper
        self._pipeline_filters_info_list = pipeline_filters_info_list
        self._workflow_api = workflow_api
        self._dsp_dataset_api = dsp_dataset_api
        self._ccs_api = ccs_api

        self._progress_manager = progress_manager

    def run(self):
        logger.debug("Ingestion in progress!")
        self._progress_manager.set_msg("Ingestion in progress!")

        ingest_step: ProgressStep = self._progress_manager.register_step(
            "Ingest", weight=self.INGEST_WORKFLOW_PROGRESS_WEIGHTAGE
        )

        process_steps: List[ProgressStep] = []
        for pipeline in self._catalog_tables_helper.get_pipeline_tables_info():
            pipeline_id = pipeline.get_pipeline_id()
            pipeline_name = pipeline.get_pipeline_name()
            process_steps.append(
                self._progress_manager.register_step(
                    f"Process-{pipeline_id}-{pipeline_name}",
                    weight=self.PROCESS_WORKFLOW_PROGRESS_WEIGHTAGE,
                )
            )

        try:
            self._run_ingest_workflow(ingest_step=ingest_step)

            self._run_process_workflow(process_steps=process_steps)

            self._progress_manager.set_msg(msg="Ingestion completed!")
        except Exception as exc:
            logger.error(f"Workflow execution failed  due to {exc}")
            raise

        logger.debug("Ingestion completed!")

    def _run_ingest_workflow(self, ingest_step: ProgressStep):
        session_id, workflow_id = WorkflowHelper.get_session_and_workflow_id(
            workflow_id_prefix="reg", dataset_id=self._dataset.id
        )

        ingest_partitioner_filter = (
            PartitionerFilterFactory.get_ingest_partitioner(
                dataset=self._dataset,
                data_dir=self._data_dir,
                session_id=session_id,
                workflow_id=workflow_id,
                dataset_tables_info=(
                    self._catalog_tables_helper.get_dataset_tables_info()
                ),
                ccs_api=self._ccs_api,
                ingest_step=ingest_step,
                data_type=get_dataset_type(
                    dataset_type=self._dataset.data_type
                ),
            )
        )

        ingest_partitioner_filter.run()

    def _run_process_workflow(self, process_steps: List[ProgressStep]):
        for index, pipeline_info in enumerate(
            self._catalog_tables_helper.get_pipeline_tables_info()
        ):
            logger.debug(
                f"Running process workflow for pipeline "
                f"{pipeline_info.get_pipeline_id()}"
            )
            (
                session_id,
                workflow_id,
            ) = WorkflowHelper.get_session_and_workflow_id(
                workflow_id_prefix="process", dataset_id=self._dataset.id
            )
            pipeline_filters_info = self._pipeline_filters_info_list[index]
            self._run_process_workflow_per_pipeline(
                pipeline_info=pipeline_info,
                pipeline_filters_info=pipeline_filters_info,
                session_id=session_id,
                workflow_id=workflow_id,
                process_step=process_steps[index],
                dataset_data_type=get_dataset_type(
                    dataset_type=self._dataset.data_type
                ),
            )

    @staticmethod
    def _is_patch_features(feaurizer_details: am.AkriSDKFilterDetails):
        feature_n = int(feaurizer_details.init_params.get("feature_n", "1"))
        feature_m = int(feaurizer_details.init_params.get("feature_m", "1"))
        return feature_n * feature_m != 1

    def _run_process_workflow_per_pipeline(
        self,
        pipeline_info: PipelineTablesInfo,
        pipeline_filters_info: am.AkriSDKWorkflowResponse,
        session_id: str,
        workflow_id: str,
        process_step: ProgressStep,
        dataset_data_type: DataType,
    ):
        dataset_tables_info = (
            self._catalog_tables_helper.get_dataset_tables_info()
        )

        process_partitioner_filter = (
            PartitionerFilterFactory.get_process_partitioner(
                dataset_id=self._dataset.id,
                pipeline_tables_info=pipeline_info,
                dataset_tables_info=dataset_tables_info,
                ccs_api=self._ccs_api,
                data_type=dataset_data_type,
                sample_frame_rate=self._dataset.dataset_spec.sample_frame_rate,
            )
        )

        token_generator = process_partitioner_filter.run()

        tokens_processed = 0

        try:
            while True:
                try:
                    process_token_info: ProcessTokenInfo = next(
                        token_generator
                    )

                    token_num = process_token_info.token_number
                    parent_dir = process_token_info.parent_dir
                    metadata_dir = process_token_info.metadata_dir
                    out_dir = process_token_info.out_dir

                    # Set total steps for the first run
                    if not process_step.has_started():
                        process_step.set_total_steps(
                            process_token_info.total_num_tokens
                        )

                    # Map to get filter output directory by filter type
                    filters_output_dir_map: dict = (
                        self._get_filters_output_dir_map(
                            partitioner_out_dir=out_dir,
                            parent_dir=parent_dir,
                            token_number=token_num,
                        )
                    )

                    filter_execution_order_list: List[
                        dict
                    ] = self._get_filter_execution_order_list(
                        pipeline_filters_info=pipeline_filters_info,
                        filters_output_dir_map=filters_output_dir_map,
                    )

                    logger.debug(
                        f"Filter execution order list is {filter_execution_order_list}"
                    )

                    for sdk_details in filter_execution_order_list:
                        self._run_filter(
                            filter_details=sdk_details["filter_details"],
                            src_dir=sdk_details["src_dir"],
                            dst_dir=sdk_details["dst_dir"],
                            filter_type=sdk_details["filter_type"],
                        )

                    # init params for data ingest would be same as featurizer
                    data_ingest_init_params = (
                        pipeline_filters_info.featurizer.init_params
                    )
                    data_ingest_output_dir = filters_output_dir_map[
                        FilterTypes.DataIngest
                    ]
                    # Run Data ingest filter
                    with tempfile.NamedTemporaryFile(dir=parent_dir) as fp:
                        logger.debug("Data ingestion filter is in progress!")

                        # windows does not allow already opened temp file.
                        # fp will be deleted along with tmp_dir
                        fp_name = fp.name
                        if is_windows_os():
                            fp.close()

                        ingest_filter = DataIngestWrapper()
                        ingest_filter.init(**data_ingest_init_params)

                        # Featurizer output will be input for data ingest filter
                        ingest_src_dir = filters_output_dir_map[
                            FilterTypes.Featurizer
                        ]

                        ingest_filter.run(
                            src_dir=ingest_src_dir,
                            dst_dir=data_ingest_output_dir,
                            tmp_file=fp_name,
                        )
                        logger.debug(
                            "Data ingestion filter completed successfully!"
                        )

                    thumbnail_aggregator_output_dir = filters_output_dir_map[
                        FilterTypes.ThumbnailAggregator
                    ]
                    # Run sink writer filter
                    logger.debug("Sync filter is in progress!")
                    sink_writer = SinkWriterFilterFactory.get_sink_writer(
                        filter_input=SinkWriterFilterInput(
                            dataset_id=self._dataset.id,
                            tables_info=SinkTablesInfo(
                                primary_abs_table=pipeline_info.get_primary_abs_table(),
                                summary_abs_table=pipeline_info.get_summary_abs_table(),
                                blob_abs_table=pipeline_info.get_blobs_abs_table(),
                            ),
                            workflow_id=workflow_id,
                            session_id=session_id,
                            pipeline_id=pipeline_info.get_pipeline_id(),
                            partition_start=process_token_info.file_info_list[
                                0
                            ].partition_start,
                            partition_end=process_token_info.file_info_list[
                                0
                            ].partition_end,
                            file_metadata_list=self._prepare_file_metadata_list(
                                process_token_info.file_info_list
                            ),
                        ),
                        api_manager=ApiManager(
                            workflow_api=self._workflow_api,
                            dsp_dataset_api=self._dsp_dataset_api,
                            ccs_api=self._ccs_api,
                        ),
                        data_type=SinkDataType(dataset_data_type.value),
                    )

                    is_patch = self._is_patch_features(
                        feaurizer_details=pipeline_filters_info.featurizer
                    )

                    ingest_output_path = DataIngestOutputPath(
                        coreset_dir=concat_file_paths(
                            data_ingest_output_dir,
                            DataIngestWrapper.DEST_CORESET_SUB_DIR,
                        ),
                        projections_dir=concat_file_paths(
                            data_ingest_output_dir,
                            DataIngestWrapper.DEST_PROJECTIONS_SUB_DIR,
                        ),
                        sketch_dir=concat_file_paths(
                            data_ingest_output_dir,
                            DataIngestWrapper.DEST_SKETCH_SUB_DIR,
                        ),
                    )

                    param_name = "patch" if is_patch else "full"
                    sink_writer_params = {f"{param_name}": ingest_output_path}

                    sink_writer.run_from_input_dir(
                        thumbnail_dir=thumbnail_aggregator_output_dir,
                        blobs_dir=metadata_dir,
                        **sink_writer_params,
                    )

                    if process_token_info.should_update_progress():
                        process_step.increment_processed_steps(completed=1)

                    process_partitioner_filter.cleanup_token(
                        token_num=token_num,
                        partition_num=process_token_info.partition_num,
                    )

                    tokens_processed += 1
                except StopIteration:
                    break
        finally:
            # If not tokens processed, set total steps to 0
            if not tokens_processed:
                process_step.set_total_steps(0)

            process_partitioner_filter.cleanup()

        # Update dsp session
        session_create_request = dsp.PipelineSessionCreateRequest(
            status="COMPLETE"
        )
        self._dsp_dataset_api.update_dataset_session_state(
            session_id=session_id,
            pipeline_id=pipeline_info.get_pipeline_id(),
            dataset_id=self._dataset.id,
            pipeline_session_create_request=session_create_request,
        )

        logger.debug(
            f"Session completed for pipeline {pipeline_info.get_pipeline_id()}!"
        )

    @staticmethod
    def _prepare_file_metadata_list(
        process_file_info_list: List[ProcessFileInfo],
    ) -> List[FileInfo]:
        return [
            FileInfo(
                file_path=process_file_info.file_path,
                file_id=process_file_info.file_id,
                frame_idx_in_blob=process_file_info.frame_idx_in_blob,
                file_name=process_file_info.file_name,
                frame_idx_in_file=process_file_info.frame_idx_in_file,
                total_frames_in_file=process_file_info.total_frames_in_file,
                frame_width=process_file_info.frame_width,
                frame_height=process_file_info.frame_height,
                native_fps=process_file_info.native_fps,
                blob_idx_in_partition=process_file_info.blob_idx_in_partition,
            )
            for process_file_info in process_file_info_list
        ]

    @classmethod
    def _get_filter_execution_order_list(
        cls,
        pipeline_filters_info: am.AkriSDKWorkflowResponse,
        filters_output_dir_map: dict,
    ) -> List[dict]:
        """
        :param pipeline_filters_info: List of Filter info that attached to
            pipeline
        :return: List[dict]:
                List of required details to run a filter where src_dir value
                refer from where to read and dst_dir value refer where to write
        """

        filter_execution_order_list = [
            {
                "filter_type": FilterTypes.Preprocessor,
                "src_dir": filters_output_dir_map[FilterTypes.Partitioner],
                "filter_details": pipeline_filters_info.pre_processor,
                "dst_dir": filters_output_dir_map[FilterTypes.Preprocessor],
            },
            {
                "filter_type": FilterTypes.Featurizer,
                "src_dir": filters_output_dir_map[FilterTypes.Preprocessor],
                "filter_details": pipeline_filters_info.featurizer,
                "dst_dir": filters_output_dir_map[FilterTypes.Featurizer],
            },
            {
                "filter_type": FilterTypes.Thumbnail,
                "src_dir": filters_output_dir_map[FilterTypes.Partitioner],
                "filter_details": pipeline_filters_info.thumbnail,
                "dst_dir": filters_output_dir_map[FilterTypes.Thumbnail],
            },
            {
                "filter_type": FilterTypes.ThumbnailAggregator,
                "src_dir": filters_output_dir_map[FilterTypes.Thumbnail],
                "filter_details": (Constants.THUMBNAIL_AGGREGATOR_SDK_DETAILS),
                "dst_dir": filters_output_dir_map[
                    FilterTypes.ThumbnailAggregator
                ],
            },
        ]

        return filter_execution_order_list

    @classmethod
    def _get_filters_output_dir_map(
        cls,
        parent_dir: str,
        token_number: int,
        partitioner_out_dir: Optional[str] = None,
    ) -> dict:
        output_dir_map = {}
        for filter_type in FilterTypes:
            if filter_type == FilterTypes.Partitioner and partitioner_out_dir:
                output_dir_map[filter_type] = partitioner_out_dir
                continue

            output_dir_map[filter_type] = get_filter_output_dir(
                par_dir=parent_dir,
                token_number=token_number,
                filter_type=filter_type.value,
            )
        return output_dir_map

    @staticmethod
    def _run_filter(
        filter_details: am.AkriSDKFilterDetails,
        src_dir: str,
        dst_dir: str,
        filter_type: FilterTypes,
    ):
        try:
            logger.debug(f"{filter_type.value} filter is in progress!")
            module = filter_details.module
            class_name = filter_details.class_name
            run_method = filter_details.run_method
            init_method = filter_details.init_method
            cleanup_method = filter_details.cleanup_method
            init_params = {}
            if filter_details.init_params:
                init_params = filter_details.init_params

            class_executor = ClassExecutor(
                module_path=module, klass_name=class_name
            )

            if init_method:
                class_executor.call_method(init_method, **init_params)

            run_method_params = {"src_dir": src_dir, "dst_dir": dst_dir}
            class_executor.call_method(run_method, **run_method_params)

            if cleanup_method:
                class_executor.call_method(method_name=cleanup_method)
            logger.debug(f"{filter_type.value} filter completed successfully!")
        except Exception as ex:
            logger.error(
                f"Failed to run sdk filter due to {ex}. Filter details {filter_details}"
            )
            raise ServerError(f"Failed to run sdk filter with error: {ex}")
