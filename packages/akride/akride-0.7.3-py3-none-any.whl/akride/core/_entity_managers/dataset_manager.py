from time import sleep
from typing import Any, Dict, List, Optional, Set

import akridata_akrimanager_v2 as am
import akridata_dsp as dsp
from akridata_akrimanager_v2 import ApiException as AMException
from akridata_akrimanager_v2 import (
    AttachmentPolicyListResp,
    AttachmentPolicyResp,
    AttachmentPolicyType,
    BCCreateJobReq,
    BCCreateJobResp,
    BCJobDetailedStatus,
    PolicyDetailsBody,
)

from akride import logger
from akride._utils.background_task_helper import BackgroundTask
from akride._utils.catalog.catalog_tables_helper import CatalogTablesHelper
from akride._utils.catalog.pipeline_tables_info import PipelineTablesInfo
from akride._utils.dataset_utils import get_dataset_type
from akride._utils.exception_utils import translate_api_exceptions
from akride._utils.progress_bar_helper import ProgressBarHelper
from akride._utils.progress_manager.manager import ProgressManager
from akride.core._entity_managers._models.datasets import CreateDatasetIn
from akride.core._entity_managers.catalog_manager import CatalogManager
from akride.core._entity_managers.manager import Manager
from akride.core._pipeline_executor import PipelineExecutor
from akride.core.entities.bgc_job import BGCJob
from akride.core.entities.datasets import Dataset
from akride.core.entities.entity import Entity
from akride.core.entities.pipeline import Pipeline
from akride.core.enums import BackgroundTaskType, DataType, FeaturizerType
from akride.core.exceptions import ServerError, UserError
from akride.core.models.bc_attachment_job_status import BGCAttachmentJobStatus
from akride.core.models.catalogs.catalog_details import CatalogDetails
from akride.core.models.datasets.get_unprocessed_files import (
    DatasetUnprocessedFiles,
)
from akride.core.models.progress_info import ProgressInfo
from akride.core.types import ClientManager


class DatasetManager(Manager):
    """
    Class Managing Dataset related operations on DataExplorer
    """

    def __init__(self, cli_manager: ClientManager):
        super().__init__(cli_manager)
        self.dataset_api = am.DatasetsApi(cli_manager.am_client)
        self.catalog_api: am.CatalogApi = am.CatalogApi(cli_manager.am_client)
        self.pipeline_api: am.PipelineApi = am.PipelineApi(
            cli_manager.am_client
        )
        self.workflow_api: am.WorkflowsApi = am.WorkflowsApi(
            cli_manager.am_client
        )
        self.bgc_api: am.BackgroundCatalogApi = am.BackgroundCatalogApi(
            cli_manager.am_client
        )
        self.dsp_dataset_api: dsp.DatasetApi = dsp.DatasetApi(
            cli_manager.dsp_client
        )
        self.ccs_api: am.CcsApi = am.CcsApi(cli_manager.am_client)
        self.attachment_policy_api = am.AttachmentPoliciesApi(
            cli_manager.am_client
        )

        self._catalogs = CatalogManager(cli_manager)

    @translate_api_exceptions
    def create_entity(self, spec: Dict[str, Any]) -> Entity:
        """
        Creates a new dataset.

        Parameters
        ----------
        spec : Dict[str, Any]
            The dataset spec.

        Returns
        -------
        Entity
            The created dataset
        """
        input_spec = CreateDatasetIn(**spec)
        return self._create_dataset(input_spec)

    def _get_default_dataset_config(self, data_type: DataType):
        params = {"data_type": data_type.value, "include_akride": True}
        return self.dataset_api.get_default_dataset_config(**params)

    def _get_featurizer_and_pipeline_mapping(
        self, data_type: DataType
    ) -> Dict[FeaturizerType, am.GetPipelineResp]:
        dataset_config: am.DefaultDatasetConfigDetails = (
            self._get_default_dataset_config(data_type=data_type)
        )
        policy_mapping: am.PolicyToPipelineMapping = (
            dataset_config.policy_to_pipeline_mapping
        )
        akride_default_pipelines: List[am.GetPipelineResp] = []
        if policy_mapping.akride:
            akride_default_pipelines = policy_mapping.akride

        featurizer_and_pipeline_mapping = {}
        for pipeline in akride_default_pipelines:
            if pipeline.pipeline_type == FeaturizerType.PATCH.value:
                featurizer_and_pipeline_mapping[
                    FeaturizerType.PATCH
                ] = pipeline
            elif pipeline.pipeline_type == FeaturizerType.FULL_IMAGE.value:
                if pipeline.featurizer_docker.properties.get("text_search"):
                    featurizer_and_pipeline_mapping[
                        FeaturizerType.CLIP
                    ] = pipeline
                else:
                    featurizer_and_pipeline_mapping[
                        FeaturizerType.FULL_IMAGE
                    ] = pipeline

        return featurizer_and_pipeline_mapping

    @translate_api_exceptions
    def delete_entity(self, entity: Entity) -> bool:
        """
        Deletes an entity.

        Parameters
        ----------
        entity : Entity
            The entity object to delete.

        Returns
        -------
        bool
            Indicates whether this entity was successfully deleted
        """
        dataset_id = entity.get_id()
        api_response = self.dataset_api.delete_dataset(dataset_id)
        return api_response.success == "True"  # type: ignore

    def _create_dataset(self, create_data: CreateDatasetIn) -> Dataset:
        """
        Method for creating a new dataset.

        Parameters
        ----------
        dataset_name : str
            The name of the new dataset.
        dataset_namespace : str, optional
            The namespace for the dataset, by default 'default'.
        data_type : DataType, optional
            The type of data to store in the dataset, by default
            DataType.IMAGE.
        glob_pattern : str, optional
            The glob pattern for the dataset, by default
            '*(png|jpg|gif|jpeg|tiff|tif|bmp)'.
        overwrite : bool, optional
            Overwrite if a dataset with the same name exists.
        sample_frame_rate: float, optional
            The frame rate per second (fps) for videos.
            Applicable only for video datasets.
        Returns
        -------
        Dataset
            The newly created dataset.
        """
        logger.debug(f"Creating dataset with input {create_data}")

        if create_data.overwrite:
            raise NotImplementedError

        dataset_spec = {
            "access_type": "default",
            "glob": create_data.glob_pattern,
        }

        if create_data.data_type == DataType.VIDEO:
            dataset_spec["sample_frame_rate"] = create_data.sample_frame_rate

        # If container id is passed, use the container to create dataset.
        # Else, create local container
        src_container = {"local": True}
        if create_data.source_container_data:
            src_container = {
                "local": False,
                "id": create_data.source_container_data.id,
            }
        containers = {"source": src_container, "sink": {"internal": True}}
        dataset_type = "basic"
        am_dataset = am.DataSet(
            dataset_name=create_data.dataset_name,
            namespace=create_data.dataset_namespace,
            type=dataset_type,
            data_type=create_data.data_type.value,
            containers=containers,
            dataset_spec=dataset_spec,
        )
        api_response = self.dataset_api.create_new_dataset(am_dataset)
        assert api_response._dataset_id is not None
        return self.get_entity_by_id(entity_id=api_response._dataset_id)

    def _get_attachment_policy(
        self, attachment_policy_type: AttachmentPolicyType
    ):
        policy_resp: AttachmentPolicyListResp = (
            self.attachment_policy_api.get_attachment_policies()
        )

        for policy in policy_resp.attachment_policies:
            if policy.type == attachment_policy_type:
                return policy

        raise UserError(f"No policy found for type {attachment_policy_type}")

    @translate_api_exceptions
    def attach_default_pipelines(
        self,
        dataset: Dataset,
        featurizers: Set[FeaturizerType],
        attachment_policy_type: Optional[AttachmentPolicyType] = None,
    ) -> None:
        """
        Attaches pipelines based on featurizers
        Parameters
        ----------
        dataset: Dataset
            The dataset object to attach pipelines
        featurizers: Set[FeaturizerType]
            Featurizers to attach
        attachment_policy_type: Optional[AttachmentPolicyType]
            Attachment policy type for the pipelines

        Returns
        -------
        None
        """
        data_type = get_dataset_type(dataset.info.data_type)

        dataset_id = dataset.get_id()

        featurizer_pipeline_mapping: Dict[
            FeaturizerType, am.GetPipelineResp
        ] = self._get_featurizer_and_pipeline_mapping(data_type=data_type)

        pipelines_to_attach = []
        for f in featurizers:
            pipeline = featurizer_pipeline_mapping.get(f)
            if not pipeline:
                raise ServerError(
                    f"Pipeline details not found for featurizer "
                    f"{f} and data type {data_type}!"
                )

            pipelines_to_attach.append(pipeline.pipeline_id)

        attachment_policy = PolicyDetailsBody()
        if attachment_policy_type:
            policy: AttachmentPolicyResp = self._get_attachment_policy(
                attachment_policy_type=attachment_policy_type
            )

            attachment_policy = PolicyDetailsBody(
                policy_id=policy.id, cluster_id=policy.cluster_id
            )

        # Create attachments
        for pipeline_id in pipelines_to_attach:
            self.pipeline_api.attach_pipeline_to_datasets(
                pipeline_id=pipeline_id,
                pipeline_attach_body=am.PipelineAttachBody(
                    dataset_ids=[dataset_id],
                    attachment_policy=attachment_policy,
                ),
            )

    def _attach_pipeline(
        self,
        dataset: Dataset,
        featurizer_type: FeaturizerType,
        with_clip_featurizer: bool,
    ) -> None:
        """
        Attaches a pipeline based on featurizer_type
        Parameters
        ----------
        dataset : Dataset
            dataset to attach.
        featurizer_type: Type of featurizer to be used for attachment
        with_clip_featurizer: bool
            attach clip pipeline

        Returns
        -------
        None
        """
        featurizers_to_attach = [featurizer_type]
        if with_clip_featurizer:
            featurizers_to_attach.append(FeaturizerType.CLIP)

        self.attach_default_pipelines(
            dataset=dataset, featurizers=set(featurizers_to_attach)
        )

    def _get_internal_pipeline_details(
        self, pipeline_internal_id: int
    ) -> Optional[am.PipelineItem]:
        # Get pipeline filter by pipeline_internal_id
        pipelines_resp: am.Pipelines = self.pipeline_api.get_all_pipelines(
            filter_by_internal_id=pipeline_internal_id
        )

        internal_pipeline = None
        if pipelines_resp.pipelines:
            internal_pipeline = pipelines_resp.pipelines[0]

        return internal_pipeline

    @translate_api_exceptions
    def get_bgc_attachment_progress_report(
        self, dataset: Dataset, pipeline: Pipeline
    ) -> BGCAttachmentJobStatus:
        """
        Get Background Catalog progress on the dataset

        Parameters
        ----------
        dataset : Dataset
            The dataset object to retrieve background catalog jobs
        pipeline: Pipeline
            The pipeline object which is attached to dataset
        Returns
        -------
        BGCAttachmentJobStatus:
            Status of the cataloging jobs for a dataset
        """

        progress_report: am.BCAttachmentProgressReportResp = (
            self.bgc_api.get_attachment_progress_report(
                dataset_id=dataset.get_id(), pipeline_id=pipeline.get_id()
            )
        )

        return BGCAttachmentJobStatus(
            job_id=progress_report.job_id,
            status=progress_report.status,
            error_logs=progress_report.error_logs,
            progress=progress_report.progress,
            start_time=progress_report.start_time,
            end_time=progress_report.end_time,
        )

    @translate_api_exceptions
    def get_bgc_job(self, job_id: str) -> BGCJob:
        """
        Get BGC job by the job id

        Parameters
        ----------
        job_id: str
            Job id of the triggered BGC job
        Returns
        -------
        BGCJob:
            The background Catalog object
        """
        resp: BCJobDetailedStatus = self.bgc_api.get_job_status(job_id=job_id)
        return BGCJob(info=resp)

    @translate_api_exceptions
    def submit_bgc_job(
        self, dataset: Dataset, pipelines: List[Pipeline]
    ) -> BGCJob:
        """
        Submits a Background Cataloging Job for the dataset

        Parameters
        ----------
        dataset : Dataset
            The dataset object to submit ingestion.
        pipelines : List[Pipeline]
            Pipelines to run for the job
        Returns
        -------
        BGCJob:
            The background Catalog object
        """

        if not pipelines:
            return None

        pipeline_id_list = [pipeline.get_id() for pipeline in pipelines]

        job_req = BCCreateJobReq(
            dataset_id=dataset.get_id(), pipeline_ids=pipeline_id_list
        )

        resp: BCCreateJobResp = self.bgc_api.create_job(
            bc_create_job_req=job_req
        )

        return self.get_bgc_job(job_id=resp.job_id)

    @translate_api_exceptions
    def abort_bgc_job(
        self,
        dataset: Dataset,
        job: Optional[BGCJob] = None,
    ):
        """
        Aborts background cataloging jobs for the dataset

        Parameters
        ----------
        dataset : Dataset
            The dataset object to submit ingestion.
        job: BGCJob
            The background catalog job object
        Returns
        -------
        None
        """

        # Abort BGC jobs for a dataset
        try:
            job_id = job.get_id() if job else None

            self.bgc_api.abort_bgc_job(
                dataset_id=dataset.get_id(), job_id=job_id
            )
        except AMException as ex:
            # Handle case when no eligible abort jobs are pending
            if ex.status == 404:
                pass

            raise ex

    @translate_api_exceptions
    def ingest_dataset(
        self,
        dataset: Dataset,
        data_directory: str,
        async_req: bool,
        with_clip_featurizer: bool,
        featurizer_type: FeaturizerType = FeaturizerType.FULL_IMAGE,
        catalog_details: Optional[CatalogDetails] = None,
    ) -> Optional[BackgroundTask]:
        """
        Starts an asynchronous ingest task for the specified dataset.
        Attaches a pipeline based on featurizer_type and executes the pipeline

        Parameters
        ----------
        dataset : Dataset
            The dataset to ingest.
        data_directory : str
            The path to the directory containing the dataset files.
        async_req: bool
            Whether to execute the request asynchronously.
        with_clip_featurizer: bool, optional
            Ingest dataset to enable text prompt based search.
        featurizer_type: Type of featurizer to be used
        catalog_details: Optional[CatalogDetails]
            parameters details for creating a catalog

        Returns
        -------
        BackgroundTask
            A task object
        """
        # Check to avoid concurrent ingestion of same dataset.
        if self.client_manager.background_task_manager.is_task_running(
            entity_id=dataset.get_id(),
            task_type=BackgroundTaskType.DATASET_INGESTION,
        ):
            raise UserError("Ingestion already in progress!")

        if catalog_details:
            self._catalogs.import_catalog(
                dataset=dataset,
                csv_file_path=catalog_details.catalog_csv_file,
                table_name=catalog_details.table_name,
            )

        self._attach_pipeline(
            dataset=dataset,
            featurizer_type=featurizer_type,
            with_clip_featurizer=with_clip_featurizer,
        )

        dataset_json = self._get_dataset_json(
            dataset_id=dataset.get_id(), version=dataset.info.latest_version
        )

        catalog_tables_resp: am.CatalogTableResponse = (
            self.catalog_api.get_catalog_tables(dataset_id=dataset.get_id())
        )
        catalog_tables_helper = CatalogTablesHelper(
            catalog_tables_resp=catalog_tables_resp
        )

        # Get filters info for all pipelines
        pipeline_filters_info_list: List[am.AkriSDKWorkflowResponse] = []
        for pipeline in catalog_tables_helper.get_pipeline_tables_info():
            pipeline_filters_info_list.append(
                self.workflow_api.get_akrisdk_details(
                    dataset_id=dataset.get_id(),
                    pipeline_id=pipeline.get_pipeline_id(),
                )
            )

        workflow_params = {
            "dataset_json": dataset_json,
            "data_dir": data_directory,
            "catalog_tables_helper": catalog_tables_helper,
            "pipeline_filters_info_list": pipeline_filters_info_list,
            "workflow_api": self.workflow_api,
            "dsp_dataset_api": self.dsp_dataset_api,
            "ccs_api": self.ccs_api,
        }

        task = self.client_manager.background_task_manager.start_task(
            entity_id=dataset.get_id(),
            task_type=BackgroundTaskType.DATASET_INGESTION,
            target_function=self._run_workflow,
            **workflow_params,
        )

        if async_req:
            return task

        previous_completed = 0
        with ProgressBarHelper(total=100) as pbar:
            while not task.has_completed():
                sleep(5)
                percent_completed = task.get_progress_info().percent_completed
                incremental_change = percent_completed - previous_completed
                pbar.update(incremental_change)
                previous_completed = percent_completed

        progress_info: ProgressInfo = task.wait_for_completion()
        if progress_info.failed:
            logger.error(
                f"Failed to ingest dataset with error: {progress_info.error}"
            )

        return task

    @staticmethod
    def _run_workflow(
        progress_manager: ProgressManager,
        dataset_json: am.DataSetJSON,
        data_dir: str,
        catalog_tables_helper: CatalogTablesHelper,
        pipeline_filters_info_list: List[am.AkriSDKWorkflowResponse],
        workflow_api: am.WorkflowsApi,
        dsp_dataset_api: dsp.DatasetApi,
        ccs_api: am.CcsApi,
    ):
        PipelineExecutor(
            dataset=dataset_json,
            data_dir=data_dir,
            catalog_tables_helper=catalog_tables_helper,
            pipeline_filters_info_list=pipeline_filters_info_list,
            workflow_api=workflow_api,
            dsp_dataset_api=dsp_dataset_api,
            ccs_api=ccs_api,
            progress_manager=progress_manager,
        ).run()

    @translate_api_exceptions
    def get_entities(self, attributes: Dict[str, Any]) -> List[Dataset]:
        """
        Retrieves information about datasets that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any]
            The filter specification. It may have the following optional
            fields: search_key : str
                    Filter across fields like dataset id, and dataset name.

        Returns
        -------
        List[Entity]
            A list of Entity objects representing datasets.
        """
        attributes = attributes.copy()
        if "data_type" in attributes:
            attributes["filter_by_datatype"] = attributes["data_type"]
            del attributes["data_type"]
        if "search_key" in attributes:
            attributes["search_str"] = attributes["search_key"]
            del attributes["search_key"]
        api_response = self.dataset_api.list_datasets(**attributes)
        dataset_list = [Dataset(info) for info in api_response.datasets]
        return dataset_list

    @translate_api_exceptions
    def get_entity_by_id(self, entity_id: str) -> Optional[Dataset]:
        """
        Retrieves information about dataset for the given ID.

        Parameters
        ----------
        entity_id: str
            Dataset Id

        Returns
        -------
        Entity
            Entity object representing dataset.
        """
        dataset_info: am.DataSetsItem = self.dataset_api.get_dataset_info(
            dataset_id=entity_id
        )

        dataset = None
        if dataset_info:
            dataset = Dataset(info=dataset_info)
        return dataset

    def _get_dataset_json(
        self, dataset_id: str, version: str
    ) -> am.DataSetJSON:
        """
        Get DataSetJSON object for dataset with given version..

        Parameters
        ----------
        dataset_id: str
            Dataset Id

        Returns
        -------
        DataSetJSON
            Dataset json details.
        """
        return self.dataset_api.get_dataset_json(
            dataset_id=dataset_id, version=version
        )  # type: ignore

    def get_default_pipeline(
        self,
        attached_pipelines: List[Pipeline],
        data_type: DataType,
    ) -> Optional[Pipeline]:
        # Find the pipelines from the list of attached pipelines based on the
        # dataset type, if both full/patch pipelines are present, prefer patch
        # pipeline
        patch_image_pipeline: Optional[Pipeline] = None
        full_image_pipeline: Optional[Pipeline] = None

        featurizer_pipeline_map = self._get_featurizer_and_pipeline_mapping(
            data_type=data_type
        )

        patch_image_pipeline_id = None
        full_image_pipeline_id = None
        if featurizer_pipeline_map.get(FeaturizerType.PATCH):
            patch_image_pipeline_id = featurizer_pipeline_map[
                FeaturizerType.PATCH
            ].internal_id

        if featurizer_pipeline_map.get(FeaturizerType.FULL_IMAGE):
            full_image_pipeline_id = featurizer_pipeline_map[
                FeaturizerType.FULL_IMAGE
            ].internal_id

        logger.info(
            f"Patch image pipeline id is {patch_image_pipeline_id},"
            f"Full image pipeline id is {full_image_pipeline_id}"
        )

        for pipeline in attached_pipelines:
            internal_id = pipeline.info.pipeline_internal_id

            logger.info(f"Internal id is {internal_id}")
            if internal_id == patch_image_pipeline_id:
                patch_image_pipeline = pipeline
                break

            if internal_id == full_image_pipeline_id:
                full_image_pipeline = pipeline

        if patch_image_pipeline is None and full_image_pipeline is None:
            raise UserError(
                message="No default pipelines attached to the dataset"
            )

        return (
            patch_image_pipeline
            if patch_image_pipeline
            else full_image_pipeline
        )

    def get_attached_pipelines(
        self, dataset: Dataset, version: Optional[str] = None
    ) -> List[Pipeline]:
        """Get pipelines applicable for  dataset given a dataset version

        Args:
            dataset (Dataset): Dataset object
            version (str, optional): Dataset version. Defaults to None in which
            case the latest version would be used

        Returns:
            List[Pipeline]: List of pipelines associated with the dataset
        """
        ds_id = dataset.get_id()
        if not version:
            ds_version: str = dataset.info.latest_version  # type: ignore
        else:
            ds_version = version
        ds_json: am.DataSetJSON = self.dataset_api.get_dataset_json(
            dataset_id=ds_id, version=ds_version
        )  # type: ignore
        pipelines = []
        for pipeline in ds_json.pipelines:  # type: ignore
            pipeline: am.Pipeline
            if pipeline.is_attached:
                pipelines.append(Pipeline(pipeline))

        return pipelines

    @translate_api_exceptions
    def attach_pipeline(
        self,
        dataset_id,
        pipeline_id,
        attachment_policy_type: Optional[
            AttachmentPolicyType
        ] = AttachmentPolicyType.ON_DEMAND,
    ):
        """Attach a pipeline to the dataset given by ID.

        Args:
            dataset_id (str): String representing a dataset id
            pipeline_id (str): String representing a pipeline id
            attachment_policy_type (AttachmentPolicyType): AttachmentPolicyType,
                defaults to AttachmentPolicyType.ON_DEMAND

        Returns:
            None
        """
        policy: AttachmentPolicyResp = self._get_attachment_policy(
            attachment_policy_type=attachment_policy_type
        )
        attachment_policy = PolicyDetailsBody(
            policy_id=policy.id, cluster_id=policy.cluster_id
        )

        # Create attachments
        self.pipeline_api.attach_pipeline_to_datasets(
            pipeline_id=pipeline_id,
            pipeline_attach_body=am.PipelineAttachBody(
                dataset_ids=[dataset_id], attachment_policy=attachment_policy
            ),
        )

    @translate_api_exceptions
    def check_if_files_to_be_ingested(
        self, dataset: Dataset, files: List[str]
    ) -> bool:
        """
        Check if files have to be ingested

        Parameters
        ----------
        dataset: Dataset
            The dataset object
        files: List[str]
            New files to register for the dataset
        Returns
        -------
        bool: Indicates whether the files need to be ingested
        """
        request_data = am.RegisterCheckpointingRequest(
            dataset_id=dataset.get_id(), file_paths=files
        )

        resp: am.RegisterCheckpointingResponse = (
            self.ccs_api.register_checkpointing_query(request_data)
        )

        return any(resp.is_file_path_unprocessed)

    @translate_api_exceptions
    def get_files_to_be_processed(
        self,
        dataset: Dataset,
        pipeline: Pipeline,
        batch_size: int,
    ) -> DatasetUnprocessedFiles:
        """
        Get files to be processed for the dataset

        Parameters
        ----------
        dataset: Dataset
            The dataset object
        pipeline: Pipeline
            The associated pipeline for which the files have to be obtained
        batch_size: int
            Number of files to be retrieved

        Returns
        -------
        DatasetUnprocessedFiles
            Dataset files to be processed.
        """
        dataset_id = dataset.get_id()
        pipeline_id = pipeline.get_id()

        catalog_tables_resp: am.CatalogTableResponse = (
            self.catalog_api.get_catalog_tables(dataset_id=dataset_id)
        )
        catalog_tables_helper = CatalogTablesHelper(
            catalog_tables_resp=catalog_tables_resp
        )
        pipeline_tables: List[
            PipelineTablesInfo
        ] = catalog_tables_helper.get_pipeline_tables_info(
            pipeline_ids={pipeline_id}
        )
        if not pipeline_tables:
            raise ServerError("Pipeline tables are not found!")

        dataset_tables = catalog_tables_helper.get_dataset_tables_info()

        primary_table = pipeline_tables[0].get_primary_abs_table()
        partition_table = dataset_tables.get_partitioned_abs_table()

        resp: am.CCSFetchUnprocessedFileNamesResponse = (
            self.ccs_api.fetch_unprocessed_file_names(
                dataset_id=dataset_id,
                batch_size=batch_size,
                primary_table=primary_table,
                partition_table=partition_table,
            )
        )

        return DatasetUnprocessedFiles(file_paths=resp.file_names)
