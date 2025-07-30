"""
 Copyright (C) 2025, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""

import json
from contextlib import suppress
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import akridata_akrimanager_v2 as am
import akridata_dsp as dsp
import pandas as pd
import urllib3
from akridata_akrimanager_v2 import AttachmentPolicyType, PipelineDocker
from akridata_akrimanager_v2.models.condition import Condition
from PIL import Image
from pyakri_de_utils.retry_helper import get_http_retry
from yarl import URL

from akride import logger
from akride._utils.background_task_helper import BackgroundTask
from akride._utils.dataset_utils import get_dataset_type
from akride._utils.proxy_utils import get_env_proxy_for_url
from akride.background_task_manager import BackgroundTaskManager
from akride.core import constants
from akride.core._entity_managers.catalog_manager import CatalogManager
from akride.core._entity_managers.container_manager import ContainerManager
from akride.core._entity_managers.dataset_manager import DatasetManager
from akride.core._entity_managers.docker_image_manager import (
    DockerImageManager,
)
from akride.core._entity_managers.job_manager import JobManager
from akride.core._entity_managers.pipeline_manager import DockerPipelineManager
from akride.core._entity_managers.repository_manager import RepositoryManager
from akride.core._entity_managers.resultset_manager import ResultsetManager
from akride.core._entity_managers.sms_manager import SMSManager
from akride.core._entity_managers.subscriptions_manager import (
    SubscriptionsManager,
)
from akride.core.entities.bgc_job import BGCJob
from akride.core.entities.catalogs import Catalog
from akride.core.entities.datasets import Dataset
from akride.core.entities.docker_image import DockerImage, DockerImageSpec
from akride.core.entities.docker_pipeline import (
    DockerPipeline,
    DockerPipelineSpec,
)
from akride.core.entities.entity import Entity
from akride.core.entities.jobs import Job, JobSpec
from akride.core.entities.pipeline import Pipeline
from akride.core.entities.resultsets import Resultset
from akride.core.entities.sms_secrets import SMSSecrets
from akride.core.exceptions import ErrorMessages, ServerError, UserError
from akride.core.models.bc_attachment_job_status import BGCAttachmentJobStatus
from akride.core.models.catalogs.catalog_details import CatalogDetails
from akride.core.models.catalogs.catalog_view_info import CatalogViewInfo
from akride.core.models.datasets.get_unprocessed_files import (
    DatasetUnprocessedFiles,
)
from akride.core.models.progress_info import ProgressInfo
from akride.core.types import (
    AnalyzeJobParams,
    CatalogTable,
    ClientManager,
    ClusterRetrievalSpec,
    Column,
    ConfusionMatrixCellSpec,
    CoresetSamplingSpec,
    JobStatistics,
    JoinCondition,
    SampleInfoList,
    SimilaritySearchSpec,
)

from akride.core.enums import (  # isort:skip
    ClusterAlgoType,
    EmbedAlgoType,
    JobContext,
    JobStatisticsContext,
    JobType,
    FeaturizerType,
    CatalogTableType,
    DataType,
    AkridataDockerNames,
)


class AkriDEClient:  # pylint:disable=R0902
    """Client class to connect to DataExplorer"""

    def __init__(
        self,
        saas_endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        sdk_config_tuple: Optional[Tuple[str, str]] = None,
        sdk_config_dict: Optional[dict] = None,
        sdk_config_file: Optional[str] = None,
    ):
        """
        Initializes the AkriDEClient with the saas_endpoint and api_key values
        The init params could be passed in different ways, incase multiple
        options are used to pass the init params the order of preference
        would be
        1. Positional params (saas_endpoint, api_key)
        2. sdk_config_tuple
        3. sdk_config
        4. sdk_config_file

        Get the sdk config by signing in to Data Explorer UI and navigating to
        Utilities → Get CLI/SDK config.

        For detailed information on how to download the SDK config refer
        https://docs.akridata.ai/docs/download-config-saas

        Parameters

        Parameters
        ----------
        saas_endpoint: str
            Dataexplorer endpoint, if None defaults to https://app.akridata.ai
        api_key: str
            api_key value obtained from Dataexplorer
        sdk_config_tuple: tuple
            A tuple consisting of saas_endpoint and api_key in that order
        sdk_config_dict: dict
            dictionary containing "saas_endpoint" and "api_key"
        sdk_config_file: str
            Path to the the SDK config file downloaded from Dataexplorer

        Raises
        ---------
            InvalidAuthConfigError: if api-key/host is invalid
            ServerNotReachableError: if the server is unreachable
        """
        try:
            app_endpoint, access_key = self._get_auth_config(
                saas_endpoint=saas_endpoint,
                api_key=api_key,
                sdk_config_tuple=sdk_config_tuple,
                sdk_config_dict=sdk_config_dict,
                sdk_config_file=sdk_config_file,
            )
        except Exception as ex:
            raise UserError(
                message=ErrorMessages.SDK_USER_ERR_01_INVALID_AUTH,
                status_code=401,
            ) from ex
        if app_endpoint is None or access_key is None:
            raise UserError(
                message=ErrorMessages.SDK_USER_ERR_01_INVALID_AUTH,
                status_code=401,
            )
        proxy, proxy_headers = self._get_proxy_url_and_headers(app_endpoint)
        app_endpoint: str = app_endpoint.split(sep="//")[1]
        self.host = app_endpoint
        self.api_key = access_key

        dsp_conf = dsp.Configuration(
            host=f"https://{app_endpoint}/ds-core",
        )
        dsp_conf.proxy = proxy  # type: ignore
        dsp_conf.proxy_headers = proxy_headers  # type: ignore
        default_retries = get_http_retry()
        dsp_conf.retries = default_retries  # type:ignore
        dsp_client = dsp.ApiClient(
            configuration=dsp_conf,
            header_name="X-API-KEY",
            header_value=access_key,
        )

        am_conf = am.Configuration(
            host=f"https://{app_endpoint}/api",
        )
        am_conf.proxy = proxy  # type: ignore
        am_conf.proxy_headers = proxy_headers  # type: ignore
        am_conf.retries = default_retries  # type:ignore
        am_client = am.ApiClient(
            configuration=am_conf,
            header_name="X-API-KEY",
            header_value=access_key,
        )

        task_manager = BackgroundTaskManager()

        cli_manager = ClientManager(
            am_client=am_client,
            dsp_client=dsp_client,
            background_task_manager=task_manager,
        )
        self.jobs = JobManager(cli_manager)
        self.resultsets = ResultsetManager(cli_manager)
        self.catalogs = CatalogManager(cli_manager)
        self.datasets = DatasetManager(cli_manager=cli_manager)
        self.subscriptions = SubscriptionsManager(cli_manager=cli_manager)
        self.sms_secrets = SMSManager(cli_manager=cli_manager)
        self.repository = RepositoryManager(cli_manager=cli_manager)
        self.containers = ContainerManager(cli_manager=cli_manager)
        self.docker_images = DockerImageManager(cli_manager=cli_manager)
        self.docker_pipelines = DockerPipelineManager(cli_manager=cli_manager)

        # Check if the api-key is valid
        self.subscriptions.get_server_version()
        logger.debug("AkriDEClient initialized")

    def _get_auth_config(
        self,
        saas_endpoint,
        api_key,
        sdk_config_tuple,
        sdk_config_dict,
        sdk_config_file,
    ):
        saas_ep, auth_key = None, None
        if api_key:
            if saas_endpoint is None:
                saas_ep = constants.Constants.DEFAULT_SAAS_ENDPOINT
            else:
                saas_ep = saas_endpoint
            auth_key = api_key
        elif sdk_config_tuple:
            saas_ep, auth_key = sdk_config_tuple
        elif sdk_config_dict:
            saas_ep, auth_key = (
                sdk_config_dict["saas_endpoint"],
                sdk_config_dict["api_key"],
            )
        elif sdk_config_file:
            with open(sdk_config_file, "r", encoding="utf-8") as api_conf:
                auth_config = json.load(api_conf)
                saas_ep, auth_key = (
                    auth_config["saas_endpoint"],
                    auth_config["api_key"],
                )
        else:
            raise TypeError(
                "AkriDEClient Initialization requires one of the following "
                " options: 'sdk_config_tuple','sdk_config_dict' "
                "or 'sdk_config_file'  "
            )

        return saas_ep, auth_key

    def _get_proxy_url_and_headers(
        self, host
    ) -> Tuple[Optional[str], Optional[Dict[str, str]]]:
        try:
            with suppress(LookupError):
                url = URL(host)
                proxy_url, proxy_basic_auth = get_env_proxy_for_url(url)
                if proxy_basic_auth:
                    return proxy_url.human_repr(), urllib3.make_headers(
                        proxy_basic_auth=proxy_basic_auth
                    )
                return proxy_url.human_repr(), None
            return None, None
        except Exception as e:
            raise e

    def get_server_version(self) -> str:
        """Get Dataexplorer server version

        Returns:
            str: server version
        """
        return self.subscriptions.get_server_version()

    #
    # Container API
    #
    def get_containers(
        self, attributes: Optional[Dict[str, Any]] = None
    ) -> List[Entity]:
        """
        Retrieves information about containers that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any], optional
            The filter specification. It may have the following
            optional fields:
                filter_by_name: str
                    Filter by container name.
                search_by_name : str
                    Search by container name.

        Returns
        -------
        List[Entity]
            A list of Entity objects representing containers.
        """
        return self.containers.get_entities(attributes)  # type: ignore

    #
    # Dataset API
    #

    def get_datasets(self, attributes: Dict[str, Any] = {}) -> List[Entity]:
        """
        Retrieves information about datasets that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any], optional
            The filter specification. It may have the following
            optional fields:
                search_key : str
                    Filter across fields like dataset id, and dataset name.

        Returns
        -------
        List[Entity]
            A list of Entity objects representing datasets.
        """
        return self.datasets.get_entities(attributes)  # type: ignore

    def get_dataset_by_name(self, name: str) -> Optional[Entity]:
        """
        Retrieves a dataset with the given name.

        Parameters
        ----------
        name : str
            The name of the dataset to retrieve.

        Returns
        -------
        Entity
            The Entity object
            representing the dataset.
        """
        return self.datasets.get_entity_by_name(name)

    def create_dataset(self, spec: Dict[str, Any]) -> Entity:
        """
        Creates a new dataset entity.

        Parameters
        ----------
        spec : Dict[str, Any]
            The dataset spec. The spec should have the following fields:
                dataset_name : str
                    The name of the new dataset.
                dataset_namespace : str, optional
                    The namespace for the dataset, by default 'default'.
                data_type : DataType, optional
                    The type of data to store in the dataset, by default
                    DataType.IMAGE.
                glob_pattern : str, optional
                    The glob pattern for the dataset, by default
                    For image datasets: value ='*(png|jpg|gif|jpeg|tiff|tif|bmp)'.
                    For video datasets: value = '*(mov|mp4|avi|wmv|mpg|mpeg|mkv)'
                sample_frame_rate: float, optional
                    The frame rate per second (fps) for videos.
                    Applicable only for video datasets.
                overwrite : bool, optional
                    Overwrite if a dataset with the same name exists.

        Returns
        -------
        Entity
            The created entity
        """
        return self.datasets.create_entity(spec)

    def delete_dataset(self, dataset: Dataset) -> bool:
        """
        Deletes a dataset object.

        Parameters
        ----------
        dataset : Dataset
            The dataset object to delete.

        Returns
        -------
        bool
            Indicates whether this entity was successfully deleted
        """
        return self.datasets.delete_entity(dataset)

    def ingest_dataset(
        self,
        dataset: Dataset,
        data_directory: str,
        use_patch_featurizer: bool = True,
        with_clip_featurizer: bool = False,
        async_req: bool = False,
        catalog_details: Optional[CatalogDetails] = None,
    ) -> Optional[BackgroundTask]:
        """
        Starts an asynchronous ingest task for the specified dataset.

        Parameters
        ----------
        dataset : Dataset
            The dataset to ingest.
        data_directory : str
            The path to the directory containing the dataset files.
        use_patch_featurizer: bool, optional
            Ingest dataset to enable patch-based similarity searches.
        with_clip_featurizer: bool, optional
            Ingest dataset to enable text prompt based search.
        async_req: bool, optional
            Whether to execute the request asynchronously.
        catalog_details: Optional[CatalogDetails]
            Parameters details for creating a catalog

        Returns
        -------
        BackgroundTask
            A task object
        """
        featurizer_type = (
            FeaturizerType.PATCH
            if use_patch_featurizer
            else FeaturizerType.FULL_IMAGE
        )

        return self.datasets.ingest_dataset(
            dataset=dataset,
            data_directory=data_directory,
            featurizer_type=featurizer_type,
            catalog_details=catalog_details,
            with_clip_featurizer=with_clip_featurizer,
            async_req=async_req,
        )

    def attach_pipelines(
        self,
        dataset: Dataset,
        featurizer_types: Set[FeaturizerType],
        attachment_policy_type: Optional[
            AttachmentPolicyType
        ] = AttachmentPolicyType.PUSH_MODE,
    ):
        """
        Attach pipelines based on the featurizer types

        Parameters
        ----------
        dataset : Dataset
            The dataset object to submit ingestion.
        featurizer_types: Set[FeaturizerType]
            Featurizers to run for the dataset
        attachment_policy_type: Optional[AttachmentPolicyType]
            Pipeline attachment policy type
        Returns
        -------
        None
        """
        self.datasets.attach_default_pipelines(
            dataset=dataset,
            featurizers=featurizer_types,
            attachment_policy_type=attachment_policy_type,
        )

    def get_bgc_job_by_id(self, job_id: str) -> BGCJob:
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
        return self.datasets.get_bgc_job(job_id=job_id)

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
        return self.datasets.submit_bgc_job(
            dataset=dataset, pipelines=pipelines
        )

    def get_bgc_attached_pipeline_progress_report(
        self, dataset: Dataset, pipeline: Pipeline
    ) -> BGCAttachmentJobStatus:
        """
        Get Background Catalog progress for the dataset attachment

        Parameters
        ----------
        dataset : Dataset
            The dataset object to retrieve background catalog jobs
        pipeline: Pipeline
            The pipeline object which is attached to dataset
        Returns
        -------
        BGCAttachmentJobStatus:
            Background Catalog status for the dataset attachment
        """

        return self.datasets.get_bgc_attachment_progress_report(
            dataset=dataset, pipeline=pipeline
        )

    def check_if_dataset_files_to_be_registered(
        self, dataset: Dataset, file_paths: List[str]
    ) -> bool:
        """
        Check if the files are not registered for the dataset

        Parameters
        ----------
        dataset: Dataset
            The dataset object
        file_paths: List[str]
            New files to register for the dataset
        Returns
        -------
        bool: Indicates if files need to be registered
        """

        return self.datasets.check_if_files_to_be_ingested(
            dataset=dataset, files=file_paths
        )

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

        return self.datasets.get_files_to_be_processed(
            dataset=dataset, pipeline=pipeline, batch_size=batch_size
        )

    def abort_bgc_jobs(self, dataset: Dataset, job: Optional[BGCJob] = None):
        """
        Aborts background cataloging jobs for the dataset

        Parameters
        ----------
        dataset : Dataset
            The dataset object to submit ingestion.
        job: Optional[BGCJob]
            The background catalog job object
        Returns
        -------
        None
        """
        self.datasets.abort_bgc_job(dataset=dataset, job=job)

    def import_catalog(
        self,
        dataset: Dataset,
        table_name: str,
        csv_file_path: str,
        create_view: bool = True,
        file_name_column: Optional[str] = None,
        pipeline_name: Optional[str] = None,
        import_identifier: Optional[str] = None,
    ) -> bool:
        """
        Method for importing an external catalog into a dataset.

        Parameters
        ----------
        dataset : Dataset
            The dataset to import the catalog into.
        table_name : str
            The name of the table to create for the catalog.
        csv_file_path : str
            The path to the CSV file containing the catalog data.
        create_view: bool default: True
            Create a view with imported catalog and primary catalog table
        file_name_column: str
            Name of the column in the csv file that
            contains the absolute filename
        pipeline_name: str
            Name of pipeline whose primary table will be joined with the
            imported table. Ignored if create_view is false
        import_identifier: str
            Unique identifier for importing data

        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        if create_view and not file_name_column:
            raise ValueError(
                "View creation requires `file_name_column` to be specified"
            )

        success = self.catalogs.import_catalog(
            dataset, table_name, csv_file_path, import_identifier
        )
        if not success:
            raise ServerError("Failed to import catalog!")

        if success and create_view:
            # find the attached image pipeline to figure out which primary
            # table is to be used to to create a view
            pipelines: List[Pipeline] = self.get_attached_pipelines(
                dataset=dataset
            )
            image_pipeline = None
            if pipeline_name is None:
                image_pipeline: Optional[
                    Pipeline
                ] = self.datasets.get_default_pipeline(
                    attached_pipelines=pipelines,
                    data_type=get_dataset_type(dataset.info.data_type),
                )
            else:
                for pipeline in pipelines:
                    pipeline: Pipeline
                    if pipeline.get_name() == pipeline_name:
                        image_pipeline = pipeline
                        break
            if not image_pipeline:
                raise UserError(
                    message=f"No pipeline {pipeline_name} attached,"
                    " If view creation is not "
                    " needed, disable it by setting `create_view` to False"
                )
            left_table = CatalogTable(
                table_name="primary",
                table_type=CatalogTableType.INTERNAL,
                pipeline_id=image_pipeline.get_id(),
            )
            right_table = CatalogTable(
                table_name=table_name, table_type=CatalogTableType.INTERNAL
            )
            join_condition = JoinCondition(
                left_column="file_name", right_column=file_name_column
            )
            _ = self.create_view(
                view_name=f"{table_name}_primary_view",
                description="Auto created view joining {table_name} "
                "with {pipeline_name} primary table",
                dataset=dataset,
                left_table=left_table,
                right_table=right_table,
                join_condition=join_condition,
            )
        return True

    def create_table(
        self,
        dataset: Dataset,
        table_name: str,
        schema: Dict[str, str],
        indices: Optional[List[str]] = None,
    ) -> str:
        """
        Adds and empty external catalog to the dataset.

        Parameters
        ----------
        dataset : Dataset
            The dataset to create the catalog in.
        table_name : str
            The name of the table to create for the catalog.
        schema : Dict[str, str]
           The schema of the external catalog table
            in the format {col_name: col_type}

        Returns
        -------
        str
            Returns the absolute table name for the external catalog.
        """
        abs_table_name = self.catalogs.create_table(
            dataset=dataset,
            table_name=table_name,
            schema=schema,
            indices=indices,
        )
        return abs_table_name

    def get_view_id(
        self, dataset: Dataset, view_name: str
    ) -> Optional[CatalogViewInfo]:
        """
        Retrieves the view id for a view of a dataset

        Parameters
        ----------
        dataset : Dataset
            The dataset to get the view id from
        view_name : str
            The name of the view, to get the id
        Returns
        -------
        Optional[CatalogViewInfo]
            Returns the CatalogViewInfo object
        """
        return self.catalogs.get_view_id(dataset=dataset, view_name=view_name)

    def add_to_catalog(
        self,
        dataset: Dataset,
        table_name: str,
        csv_file_path: str,
        import_identifier: Optional[str] = None,
    ) -> bool:
        """
        Adds new items to an existing catalog.

        Parameters
        ----------
        dataset : Dataset
            The dataset to import the catalog into.
        table_name : str
            The name of the table to create for the catalog.
        csv_file_path : str
            The path to the CSV file containing new catalog data.
        import_identifier: str
            Unique identifier for importing data

        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        return self.catalogs.add_to_catalog(
            dataset,
            table_name,
            csv_file_path,
            import_identifier=import_identifier,
        )

    def delete_catalog(self, catalog: Catalog) -> bool:
        """
        Deletes a catalog object.

        Parameters
        ----------
        catalog : Catalog
            The catalog object to delete.

        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        return self.catalogs.delete_entity(catalog)

    def get_catalogs(self, attributes: Dict[str, Any] = {}) -> List[Entity]:
        """
        Retrieves information about catalogs that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any]
            The filter specification. It may have the following optional
            fields:
                name : str
                    filter by catalog name
                status : str
                    filter by catalog status, can be one of
                    "active","inactive", "refreshing", "offline",
                    "invalid-config"

        Returns
        -------
        List[Entity]
            A list of Entity objects representing catalogs.
        """
        return self.catalogs.get_entities(attributes)

    def get_catalog_by_name(
        self, dataset: Dataset, name: str
    ) -> Optional[Entity]:
        """
        Retrieves a catalog with the given name.

        Parameters
        ----------
        dataset : Dataset
            The dataset to retrieve the catalog from.
        name : str
            The name of the catalog to retrieve.

        Returns
        -------
        Entity
            The Entity object representing the catalog.
        """
        return self.catalogs.get_catalog_by_name(dataset, name)

    def get_catalog_data_count(
        self,
        dataset: Dataset,
        table_name: str,
        filter_str: Optional[str] = None,
    ) -> int:
        """
        Retrieves the count of the number of rows in a catalog table based on filters

        Parameters
        ----------
        dataset: Dataset
            The dataset to import the catalog into.
        table_name: str
            The catalog table name
        filter_str: str
            Filter the rows based on values

        Returns
        -------
        int
            The number of rows filtered
        """
        return self.catalogs.get_catalog_data_count(
            dataset=dataset, table_name=table_name, filter_str=filter_str
        )

    def get_resultset_by_id(self, resultset_id: str) -> Entity:
        """
        Retrieves a resultset with the given identifier.

        Parameters
        ----------
        name : str
            The name of the resultset to retrieve.

        Returns
        -------
        Entity
            The Entity object representing the resultset.
        """
        return self.resultsets.get_resultset_by_id(resultset_id)

    def get_resultsets(self, attributes: Dict[str, Any] = {}) -> List[Entity]:
        """
        Retrieves information about resultsets that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any], optional
            The filter specification. It may have the following
            optional fields:
                search_key : str
                    Filter across fields like dataset id, and dataset name.

        Returns
        -------
        List[Entity]
            A list of Entity objects representing resultsets.
        """
        return self.resultsets.get_entities(attributes)  # type: ignore

    def get_resultset_by_name(self, name: str) -> Optional[Entity]:
        """
        Retrieves a resultset with the given name.

        Parameters
        ----------
        name : str
            The name of the resultset to retrieve.

        Returns
        -------
        Entity
            The Entity object representing the resultset.
        """
        return self.resultsets.get_entity_by_name(name)

    def get_resultset_samples(
        self, resultset: Resultset, max_sample_size: int = 10000
    ) -> SampleInfoList:
        """
        Retrieves the samples of a resultset

        Parameters
        ----------
        resultset : Resultset
            The Resultset object to get samples for.

        Returns
        -------
        SampleInfoList
            A SampleInfoList object.
        """
        return self.resultsets.get_samples(resultset, max_sample_size)

    def create_resultset(self, spec: Dict[str, Any]) -> Entity:
        """
        Creates a new resultset entity.

        Parameters
        ----------
        spec : Dict[str, Any]
            The resultset spec. The spec should have the following fields:
                job: Job
                    The associated job object.
                name : str
                    The name of the new resultset.
                samples: SampleInfoList
                    The samples to be included in this resultset.

        Returns
        -------
        Entity
            The created entity
        """
        return self.resultsets.create_entity(spec)  # type: ignore

    def update_resultset(
        self,
        resultset: Resultset,
        add_list: Optional[SampleInfoList] = None,
        del_list: Optional[SampleInfoList] = None,
    ) -> bool:
        """
        Updates a resultset.

        Parameters
        ----------
        resultset: Resultset
            The resultset to be updated.
        add_list: SampleInfoList, optional
            The list of samples to be added.
        del_list: SampleInfoList, optional
            The list of samples to be deleted.

        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        return self.resultsets.update_resultset(resultset, add_list, del_list)

    def delete_resultset(self, resultset: Resultset) -> bool:
        """
        Deletes a resultset object.

        Parameters
        ----------
        resultset : Resultset
            The resultset object to delete.

        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        return self.resultsets.delete_entity(resultset)  # type: ignore

    def publish_resultset(self, resultset: Resultset) -> bool:
        """
        Publishes a resultset.

        Parameters
        ----------
        resultset: Resultset
            The resultset to be published.
        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        return self.resultsets.publish(resultset=resultset)

    #
    # Job API
    #

    def create_job_spec(
        self,
        dataset: Dataset,
        job_type: Union[str, JobType] = JobType.EXPLORE,
        job_name: str = "",
        predictions_file: str = "",
        cluster_algo: Union[str, ClusterAlgoType] = ClusterAlgoType.HDBSCAN,
        embed_algo: Union[str, EmbedAlgoType] = EmbedAlgoType.UMAP,
        num_clusters: Optional[int] = None,
        max_images: int = 1000,
        catalog_table: Optional[CatalogTable] = None,
        analyze_params: Optional[AnalyzeJobParams] = None,
        pipeline: Optional[Pipeline] = None,
        filters: List[Condition] = None,  # type: ignore
        reference_job: Job = None,
    ) -> JobSpec:
        """
        Creates a JobSpec object that specifies how a job is to be created.

        Parameters:
        -----------
        dataset: Dataset
            The dataset to explore.
        job_type : JobType, optional
            The job type
        job_name : str, optional
            The name of the job to create. A unique name will be generated
            if this is not given.
        predictions_file: str, optional
            The path to the catalog file containing predictions and ground
            truth. This file must be formatted according to the specification
            at:
         https://docs.akridata.ai/docs/analyze-job-creation-and-visualization
        cluster_algo : ClusterAlgoType, optional
            The clustering algorithm to use.
        embed_algo : EmbedAlgoType, optional
            The embedding algorithm to use.
        num_clusters : int, optional
            The number of clusters to create.
        max_images : int, optional
            The maximum number of images to use.
        catalog_table: CatalogTable, optional
            The catalog to be used for creating this explore job. This defaults
            to the internal primary catalog that is created automatically when
            a dataset is created.
            default: "primary"
        analyze_params: AnalyzeJobParams, optional
            Analyze job related configuration parameters
        filters : List[Condition], optional
            The filters to be used to select a subset of samples for this job.
            These filters are applied to the catalog specified by catalog_name.
        reference_job: Job, optional
            The reference job for this compare job
        """
        if pipeline is None:
            pipelines: List[Pipeline] = self.get_attached_pipelines(
                dataset=dataset
            )
            pipeline = self.datasets.get_default_pipeline(
                attached_pipelines=pipelines,
                data_type=get_dataset_type(dataset.info.data_type),
            )
        if catalog_table is None:
            catalog_table = CatalogTable(table_name="primary")

        is_compare = False

        if job_type == JobType.COMPARE:
            is_compare = True
            job_type = JobType.EXPLORE

        return JobSpec(
            dataset=dataset,
            job_type=job_type,
            job_name=job_name,
            predictions_file=predictions_file,
            cluster_algo=cluster_algo,
            embed_algo=embed_algo,
            num_clusters=num_clusters,
            max_images=max_images,
            catalog_table=catalog_table,
            filters=filters,
            pipeline=pipeline,
            analyze_params=analyze_params,
            is_compare=is_compare,
            reference_job=reference_job,
        )

    def create_job(self, spec: JobSpec) -> Job:
        """
        Creates an explore job for the specified dataset.

        Parameters:
        -----------
        dataset: Dataset
            The dataset to explore.
        spec: JobSpec
            The job specification.

        Returns:
        --------
        Job
            The newly created Job object.
        """
        return self.jobs.create_entity(spec)  # type: ignore

    def delete_job(self, job: Job) -> bool:
        """
        Deletes a job object.

        Parameters
        ----------
        job : Job
            The job object to delete.

        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        raise NotImplementedError

    def get_job_by_name(self, name: str) -> Job:
        """
        Retrieves a job with the given name.

        Parameters
        ----------
        name : str
            The name of the job to retrieve.

        Returns
        -------
        Entity
            The Entity object representing the job.
        """
        return self.jobs.get_entity_by_name(name)  # type: ignore

    def get_jobs(self, attributes: Dict[str, Any] = {}) -> List[Entity]:
        """
        Retrieves information about jobs that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any]
            The filter specification. It may have the following
            optional fields:
                data_type : str
                    The data type to filter on. This can be 'IMAGE' or 'VIDEO'.
                job_type : str
                    The job type to filter on - 'EXPLORE', 'ANALYZE' etc.
                search_key : str
                    Filter jobs across fields like job name, dataset id, and
                    dataset name.

        Returns
        -------
        List[Entity]
            A list of Entity objects representing jobs.
        """
        return self.jobs.get_entities(attributes)  # type: ignore

    def get_compatible_reference_jobs(
        self,
        dataset: Dataset,
        pipeline: Pipeline,
        catalog_table: CatalogTable,
        search_key: str = None,
    ) -> List[Job]:
        """
        Retrieves jobs created from a given catalog_table which can be used to
        create “JobType.COMPARE” job types

        Parameters
        ----------
        dataset: Dataset
            The dataset to explore.
        pipeline: Pipeline
            The pipeline to use.
        catalog_table:
            The catalog table to use for creating compare job.
        search_key: str
            Filter jobs across fields like job name

        Returns
        -------
        List[Entity]
            A list of Entity objects representing jobs.
        """

        return self.jobs.get_compatible_reference_jobs(
            dataset, pipeline, catalog_table, search_key
        )

    def get_thumbnail_images(
        self, samples: SampleInfoList
    ) -> List[Image.Image]:
        """
        Retrieves the thumbnail images corresponding to the samples.

        Parameters
        ----------
        samples : SampleInfoList
            The samples to retrieve thumbnails for.

        Returns
        -------
        List[Image.Image]
            A list of thumbnail images.
        """
        if samples.job_id:
            return self.jobs.get_thumbnail_images(samples)
        return self.resultsets.get_thumbnail_images(samples)

    def get_fullres_images(self, samples: SampleInfoList) -> List[Image.Image]:
        """
        Retrieves the full-resolution images for the provided job.

        Parameters
        ----------
        samples : SampleInfoList
            The samples to retrieve images for.

        Returns
        -------
        List[Image.Image]
            A list of images.
        """
        return self.jobs.get_fullres_images(samples)

    def get_fullres_image_urls(self, samples: SampleInfoList) -> Dict:
        """
        Retrieves the full-resolution image urls for the give samples.

        Parameters
        ----------
        samples : SampleInfoList
            The samples to retrieve full res image urls for.

        Returns
        -------
        Dict
            A dictionary containing the full-resolution image URLs for
            each sample.
        """
        if not samples:
            raise ValueError("'samples' cannot be None")
        if not isinstance(samples, SampleInfoList):
            raise TypeError(
                f"Invalid argument type: {type(samples)}."
                f"Expected type: SampleInfoList".format(type(samples))
            )
        return self.jobs.get_fullres_image_urls(samples)

    def get_catalog_tags(self, samples: SampleInfoList) -> pd.DataFrame:
        """
        Retrieves the catalog tags corresponding to the given samples.

        Parameters
        ----------
        samples : SampleInfoList
            The samples to retrieve catalog tags for.

        Returns
        -------
        pd.DataFrame
            A dataframe of catalog tags.
        """
        return self.catalogs.get_catalog_tags(samples)

    def get_job_statistics(
        self, job: Job, context: JobStatisticsContext, **kwargs
    ) -> JobStatistics:
        """
        Retrieves statistics info from an analyze job.

        Parameters
        ----------
        job : Job
            The Job object to get statistics for.
        context: JobStatisticsContext
            The type of statistics to retrieve.
        **kwargs: Additional keyword arguments
        Supported keyword arguments
            iou_config_threshold: float, optional
                Threshold value for iou config
            confidence_score_threshold: float, optional
                Threshold value for confidence score

        Returns
        -------
        JobStatistics
            A job statistics object.
        """
        return self.jobs.get_job_statistics(job, context, **kwargs)

    def get_job_samples(
        self,
        job: Job,
        job_context: JobContext,
        spec: Union[
            SimilaritySearchSpec,
            ConfusionMatrixCellSpec,
            ClusterRetrievalSpec,
            CoresetSamplingSpec,
        ],
        **kwargs,
    ) -> SampleInfoList:
        """
        Retrieves the samples according to the given specification.

        Parameters
        ----------
        job : Job
            The Job object to get samples for.
        job_context: JobContext
            The context in which the samples are requested for.
        spec: Union[
            SimilaritySearchSpec,
            ConfusionMatrixCellSpec,
            ClusterRetrievalSpec,
            CoresetSamplingSpec
        ]
            The job context spec.
        **kwargs: Additional keyword arguments
        Supported keyword arguments
            iou_config_threshold: float, optional
                Threshold value for iou config
            confidence_score_threshold: float, optional
                Threshold value for confidence score
        Returns
        -------
        SampleInfoList
            A SampleInfoList object.
        """
        return self.jobs.get_samples(job, job_context, spec, **kwargs)

    def get_job_samples_from_file_path(
        self,
        job: Job,
        file_info: List[str],
    ) -> Dict:
        """
        Retrieves the samples according to the given specification.

        Parameters
        ----------
        job : Job
            The Job object to get samples for.
            The job context spec.
        file_info: List[str]
            List of file_paths for the images of interest
        Returns
        -------
        Dict
            dictionary of map between file_path and point_ids
        """
        return self.jobs.get_samples_from_file_path(job, file_info)

    def get_job_display_panel(
        self,
        job: Job,
    ) -> str:
        """
        Retrieves the job panel URI the Data Explorer.

        Parameters
        ----------
        job : Job
            The Job object to be queried.
        Returns
        -------
        str
            The job panel URL.
        """

        return (
            f"https://{self.host}/"
            f"{self.jobs.get_job_display_panel_uri(job)}"
        )

    #
    # Common API
    #

    def get_progress_info(self, task: BackgroundTask) -> ProgressInfo:
        """
        Gets the progress of the specified task.

        Parameters
        ----------
        task : BackgroundTask
            The task object to retrieve the progress information for.

        Returns
        -------
        ProgressInfo
            The progress information
        """
        return task.get_progress_info()

    def wait_for_completion(self, task: BackgroundTask) -> ProgressInfo:
        """
        Waits for the specified task to complete.

        Parameters
        ----------
        task : BackgroundTask
            The ID of the job to wait for.

        Returns
        -------
        ProgressInfo
            The progress information
        """
        return task.wait_for_completion()

    def create_view(
        self,
        view_name: str,
        description: Optional[str],
        dataset: Dataset,
        left_table: CatalogTable,
        right_table: CatalogTable,
        join_condition: JoinCondition,
        inner_join: bool = False,
    ) -> str:  # -> Any | None:# -> Any | None:
        """Create a SQL view for visualization
        Note: Left join is used by default while creating the view

        Args:
            view_name (str): Name of the view to create
            description (Optional[str]): Description text
            dataset (Dataset): Dataset object
            left_table (TableInfo): Left Table of the create view query
            right_table (TableInfo): Right Table of the create view query
            join_condition (JoinCondition): JoinCondition which includes the
            column from the left and the right table
            inner_join (bool): Use inner join for joining the tables

        Returns:
            str: view id
        """
        return self.catalogs.create_view(
            view_name,
            description,
            dataset,
            left_table,
            right_table,
            join_condition,
            inner_join,
        )

    def get_attached_pipelines(
        self, dataset: Dataset, version: Optional[str] = None
    ) -> List[Pipeline]:
        """Get pipelines attached for dataset given a dataset version

        Args:
            dataset (Dataset): Dataset object
            version (str, optional): Dataset version. Defaults to None in which
            case the latest version would be used

        Returns:
            List[Pipeline]: List of pipelines attached with the dataset
        """
        return self.datasets.get_attached_pipelines(dataset, version)

    def get_all_columns(
        self, dataset: Dataset, table: CatalogTable
    ) -> List[Column]:
        """Returns all columns for a table/view

        Args:
            dataset (Dataset): Dataset object
            table (TableInfo): Table Information

        Returns:
            List[Column]: List of columns of the table
        """
        return self.catalogs.get_all_columns(dataset, table)

    def get_secrets(self, name: str, namespace: str) -> Optional[SMSSecrets]:
        """
        Retrieves information about SMS Secret for
        the given SMS secret name and namespace.

        Parameters
        ----------
        name: str
             Filter across SMS Secret Key
        namespace: str
            Filter across SMS Secret Namespace

        Returns
        -------
        SMSSecrets
            Object representing Secrets.
        """
        attributes = {"sms_key": name, "sms_namespace": namespace}
        secrets = self.sms_secrets.get_entities(attributes)
        if len(secrets):
            return secrets[0]
        return None

    def get_repository_by_name(self, name: str) -> Optional[Entity]:
        """
        Retrieves a Docker repository with the given name.

        Parameters
        ----------
        name : str
            The name of the Repository to retrieve.

        Returns
        -------
        Entity
            Object representing the Docker Repository.
        """
        return self.repository.get_entity_by_name(name)

    def get_docker_image(self, name: str) -> Optional[Entity]:
        """
        Retrieves a Docker Image with the given name.

        Parameters
        ---------
        name : str
            The name of the Docker Image to retrieve

        Returns
        ------
        Entity
            The Entity object representing the Docker Image.
        """
        return self.docker_images.get_entity_by_name(name)

    def create_featurizer_image_spec(
        self,
        image_name: str,
        description: str,
        command: str,
        repository_name: str,
        properties: Dict[str, Any],
        gpu_filter: Optional[bool] = None,
        gpu_mem_fraction: Optional[float] = None,
        allow_no_gpu: Optional[bool] = None,
        namespace: Optional[str] = "default",
        image_tag: Optional[str] = "latest",
        name: Optional[str] = None,
    ) -> DockerImageSpec:
        """
        Creates a DockerImageSpec object that specifies the
        Featurizer Docker Image to be created

        Parameters:
        -----------

        image_name : str
            The name of the Docker Image present in the repository
        description : str
            A short description of the Docker Image
        command: str
            Command that is used to run the featurizer docker
        repository_name: str
            Name of the repository in DE, the Docker Image will be pulled from.
        properties: Dict[str, Any]
            Properties specific to the Docker Image
        gpu_filter: Optional[bool]
            Flag to specify if the Image can be on a GPU or not
        gpu_mem_fraction: Optional[float]
            The GPU specifying the memory to be reserved for the Docker Image.
            Should be > 0 and <= 1
        allow_no_gpu: Optional[bool]
            Flag to specify if the Image can also be run if no GPU is available
        namespace: Optional[str]
            Namespace of the Docker Image, By default it
            will be 'default'
        image_tag: Optional[str]
            Tag of the docker Image in the docker repository,
            be default it will be "latest"
        name: Optional[str]
            Display name of the Docker Image on DE,
            by default it will be same as image_name

        Returns
        ------
        DockerImageSpec
            Object representing a Docker Image Specification

        """
        resolved_repository = self.get_repository_by_name(name=repository_name)

        if not resolved_repository:
            raise ValueError("Repository does not exist")

        repository_id = resolved_repository.id
        return DockerImageSpec(
            name=name,
            namespace=namespace,
            repository_id=repository_id,
            description=description,
            image_name=image_name,
            image_tag=image_tag,
            command=command,
            properties=properties,
            gpu_filter=gpu_filter,
            gpu_mem_fraction=gpu_mem_fraction,
            allow_no_gpu=allow_no_gpu,
        )

    def register_docker_image(
        self, spec: DockerImageSpec
    ) -> Optional[DockerImage]:
        """
        Registers a Docker Image

         Parameters
         ---------
         spec : DockerImageSpec
             Docker Image Specification

         Returns
         ------
         DockerImage
             Object representing the Docker Image
        """
        return self.docker_images.create_entity(spec)  # type: ignore

    def create_featurizer_pipeline_spec(
        self,
        pipeline_name: str,
        pipeline_description: str,
        featurizer_name: str,
        data_type: Optional[str] = DataType.IMAGE,
        namespace: Optional[str] = "default",
    ) -> DockerPipelineSpec:
        """
        Creates a DockerImageSpec object that specifies
        the Featurizer Docker Image to be created

        Parameters:
        -----------

        pipeline_name : str
            The name of the Docker pipeline
        pipeline_description : str
            A short description of the Docker Pipeline
        featurizer_name: str
            Docker Image name of the featurizer to uniquely identify the image.
        data_type: Optional[str]
            Data Type of the pipeline, by default DataType.IMAGE.
            Allowed values are DataType.IMAGE, DataType.VIDEO
        namespace: Optional[str]
            Namespace of the Docker Pipeline, By default it will be 'default'
        Returns
        ------
        DockerPipelineSpec
            Object representing a Docker Pipeline Specification

        """
        featurizer_docker_resp = self.get_docker_image(name=featurizer_name)
        if not featurizer_docker_resp:
            raise ValueError(f"Featurizer - {featurizer_name} does not exist")
        pre_processor_docker_resp = self.get_docker_image(
            name=AkridataDockerNames.AKRIDATA_IMAGE_PREPROCESSOR
        )
        if not pre_processor_docker_resp:
            raise ValueError("Error Fetching Preprocessor Image")

        thumbnail_docker_resp = self.get_docker_image(
            name=AkridataDockerNames.AKRIDATA_THUMBNAIL_GENERATOR
        )
        if not thumbnail_docker_resp:
            raise ValueError("Error Fetching Thumbnail Image")

        featurizer_pipeline_docker = PipelineDocker(
            id=featurizer_docker_resp.id
        )
        preprocessor_pipeline_docker = PipelineDocker(
            id=pre_processor_docker_resp.id
        )
        thumbnail_pipeline_docker = PipelineDocker(id=thumbnail_docker_resp.id)

        return DockerPipelineSpec(
            pipeline_name=pipeline_name,
            pipeline_description=pipeline_description,
            featurizer_docker=featurizer_pipeline_docker,
            pre_processor_docker=preprocessor_pipeline_docker,
            thumbnail_docker=thumbnail_pipeline_docker,
            data_type=data_type,
            namespace=namespace,
        )

    def create_docker_pipeline(
        self, spec: DockerPipelineSpec
    ) -> Optional[DockerPipeline]:
        """
        Creates a Pipeline using the Docker Image

         Parameters
         ---------
         spec : DockerPipelineSpec
             Pipeline Specification

         Returns
         ------
         DockerPipeline
            object representing the Docker Pipeline
        """
        return self.docker_pipelines.create_entity(spec)  # type: ignore

    def attach_pipeline_to_dataset(
        self,
        pipeline_id,
        dataset_id,
        attachment_policy_type: Optional[
            AttachmentPolicyType
        ] = AttachmentPolicyType.ON_DEMAND,
    ):
        """
        Attach pipeline based on a

        Parameters
        ----------
        dataset_id : str
            The dataset id representing a dataset
        pipeline_id: str
            The pipeline id representing a docker pipeline
        attachment_policy_type: Optional[AttachmentPolicyType]
            Pipeline attachment policy type, by default "ON_DEMAND"
        Returns
        -------
        None
        """
        self.datasets.attach_pipeline(
            dataset_id=dataset_id,
            pipeline_id=pipeline_id,
            attachment_policy_type=attachment_policy_type,
        )
