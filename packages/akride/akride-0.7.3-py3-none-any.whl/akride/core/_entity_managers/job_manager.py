# flake8: noqa  E501
import io
import json
import time
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

import akridata_akrimanager_v2 as am
import akridata_dsp as dsp
import numpy as np
from akridata_akrimanager_v2 import Condition
from akridata_dsp import (
    CatalogRefineResponse,
    CatalogSourceFilter,
    CatalogTagSourceResponse,
    ColumnData,
    CreateCatalogSourceRefine,
    CreateSimSearchResponseV2,
    GetDatasetRequestResponse,
    RequestCatalogTagFilterSourceResp,
    RequestPlot,
)
from PIL import Image

from akride._utils.exception_utils import translate_api_exceptions
from akride._utils.job_creator import JobCreator
from akride.core._entity_managers.manager import Manager
from akride.core.entities.datasets import Dataset
from akride.core.entities.entity import Entity
from akride.core.entities.jobs import Job, JobSpec
from akride.core.entities.pipeline import Pipeline
from akride.core.exceptions import ServerError, UserError
from akride.core.types import (
    AnalyzeJobParams,
    CatalogTable,
    ClientManager,
    ClusterRetrievalSpec,
    ConfusionMatrix,
    ConfusionMatrixCellSpec,
    CoresetSamplingSpec,
    JobStatistics,
    SampleInfoList,
    SimilaritySearchSpec,
)

from akride.core.enums import (  # isort:skip
    JobContext,
    JobStatisticsContext,
    ClusterAlgoType,
    EmbedAlgoType, JobType,
)

class CatalogFilterStatus(Enum):
    PROCESSING = "PROCESSING"
    COMPLETE = "COMPLETE"
    UNRECOVERABLE_FAILURE = "UNRECOVERABLE_FAILURE"
    RECOVERABLE_FAILURE = "RECOVERABLE_FAILURE"
    EXPIRED = "EXPIRED"

class JobManager(Manager):
    """Class managing job related operations on DataExplorer"""

    def __init__(self, cli_manager: ClientManager):
        super().__init__(cli_manager)
        self.job_request_api: dsp.JobRequestsApi = dsp.JobRequestsApi(
            cli_manager.dsp_client
        )
        self.request_api: dsp.RequestApi = dsp.RequestApi(
            cli_manager.dsp_client
        )
        self.qms_api: am.QueriesApi = am.QueriesApi(cli_manager.am_client)
        self.catalog_api: am.CatalogApi = am.CatalogApi(cli_manager.am_client)
        self.image_fetch_api: dsp.ImageFetchApi = dsp.ImageFetchApi(
            cli_manager.dsp_client
        )
        self.request_stat_api: dsp.RequestStatisticsApi = (
            dsp.RequestStatisticsApi(cli_manager.dsp_client)
        )
        self.views_api: am.ViewsApi = am.ViewsApi(
            api_client=cli_manager.am_client
        )
        self.job_creator = JobCreator(
            request_api=self.request_api,
            job_req_api=self.job_request_api,
            qms_api=self.qms_api,
            catalog_api=self.catalog_api,
            views_api=self.views_api,
        )
        self.search_api: dsp.SimSearchRequestV2Api = dsp.SimSearchRequestV2Api(
            cli_manager.dsp_client
        )
        self.scenario_api = dsp.ScenarioApi(cli_manager.dsp_client)
        self.scenario_exec_api = dsp.ScenarioExecutionApi(
            cli_manager.dsp_client
        )
        self.resultset_api = dsp.ResultsetApi(cli_manager.dsp_client)
        self.catalog_source_tag_api = dsp.CatalogSourceTagApi(
            cli_manager.dsp_client
        )

    @translate_api_exceptions
    def create_entity(self, spec: JobSpec) -> Optional[Entity]:
        """
        Creates a new job.

        Parameters
        ----------
        spec: JobSpec
            The job specification.

        Returns
        -------
        Entity
            The created job
        """
        return self._create_job(**spec)

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

        # TODO return True only if response is 200
        return True

    def _create_job(
        self,
        dataset: Dataset,
        job_type: JobType,
        job_name: str,
        cluster_algo: str,
        embed_algo: str,
        catalog_table: CatalogTable,
        pipeline: Pipeline,
        num_clusters: Optional[int] = None,
        analyze_params: Optional[AnalyzeJobParams] = None,
        max_images: int = 1000,
        predictions_file: str = "",
        filters: Optional[List[Condition]] = None,
        is_compare: bool = False,
        reference_job: Job = None,
    ) -> Optional[Job]:
        request, response = self.job_creator.create_job(
            job_type=job_type,
            job_name=job_name,
            dataset_id=dataset.get_id(),  # type: ignore
            pipeline_id=pipeline.get_id(),  # type: ignore
            clusterer_algo=cluster_algo,
            embedder_algo=embed_algo,
            catalog_table=catalog_table,
            max_images=max_images,
            num_clusters=num_clusters,
            analyze_params=analyze_params,
            is_compare=is_compare,
            reference_job=reference_job,
            filters=filters,
        )
        job = Job(info=request)  # type: ignore
        job.id = response.rid
        job.name = job_name
        return job

    @translate_api_exceptions
    def get_entities(self, attributes: Dict[str, Any]) -> List[Job]:
        """
        Retrieves information about jobs that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any]
            The filter specification. It may have the following optional
            fields:
                data_type : str
                    The data type to filter on.
                job_type : str
                    The job type to filter on.
                search_key : str
                    Filter jobs across fields like job name, dataset id, and
                    dataset name.

        Returns
        -------
        List[Entity]
            A list of Entity objects representing jobs.
        """
        attributes = attributes.copy()
        if "data_type" in attributes:
            # the API expects this to be a list
            attributes["data_type"] = attributes["data_type"].lower()
        api_response = self.job_request_api.list_requests(**attributes)
        job_list = []
        for info in api_response.requests:
            job = Job(info)
            job.id = info.reqid
            job.name = info.reqname
            job_list.append(job)
        return job_list

    @translate_api_exceptions
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
        vcs_view_id = None
        if catalog_table.is_view:
            view_details = self.job_creator.find_required_view(
                dataset_id=dataset.id, catalog_table=catalog_table
            )
            vcs_view_id = view_details.view_id

        api_response = self.request_api.get_compatible_ref_jobs_on_query(
            dataset_id=dataset.id,
            pipeline_id=pipeline.id,
            vcs_catalog_table_name=catalog_table.table_name
            if not catalog_table.is_view
            else None,
            vcs_view_id=vcs_view_id,
            search_key=search_key,
            archived=True,
        )
        job_list = []
        for info in api_response.requests:
            job = Job(info)
            job.id = info.reqid
            job.name = info.reqname
            job_list.append(job)
        return job_list

    @translate_api_exceptions
    def get_thumbnail_images(
        self, samples: SampleInfoList
    ) -> List[Image.Image]:
        """
        Retrieves the thumbnail images for the provided job.
        Parameters
        ----------
        samples : SampleInfoList
            The samples to retrieve thumbnails for.

        Returns
        -------
        List[Image.Image]
            A list of thumbnail images.
        """
        job_id = samples.job_id
        thumbnails = dsp.Thumbnails(samples.get_point_ids())
        api_response = self.request_api.get_thumbnails(
            rid=job_id, thumbnails=thumbnails
        )
        result = []
        # TODO use the async API instead
        for image_path in api_response.data:  # type: ignore
            image_path = image_path.replace("/ds/images/", "")
            image_response = self.image_fetch_api.fetch_image(
                image_path, _preload_content=False
            )
            result.append(Image.open(io.BytesIO(image_response.data)))  # type: ignore
        return result

    @translate_api_exceptions
    def get_fullres_images(self, samples: SampleInfoList) -> List[Image.Image]:
        """
        Retrieves the full-resolution images for the provided job.

        Parameters
        ----------
        job : Job
            The Job for which to retrieve image.
        samples : SampleInfoList
            The samples to retrieve images for.

        Returns
        -------
        List[Image.Image]
            A list of images.
        """
        job_id = samples.job_id
        images = dsp.Thumbnails(samples.get_point_ids())
        req_details: (
            GetDatasetRequestResponse
        ) = self.request_api.get_request_details(
            rid=job_id,
        )  # type: ignore
        if not req_details.dataset_is_highres_accessible:
            raise UserError(
                "Full resolution images are not accessible for this dataset"
            )
        api_response = self.request_api.get_images(rid=job_id, images=images)
        result = []
        # TODO use the async API instead
        assert api_response is not None
        for image_path in api_response.data:  # type: ignore
            image_path = image_path.replace("/ds/images/", "")
            image_response = self.image_fetch_api.fetch_image(
                image_path, _preload_content=False
            )
            result.append(Image.open(io.BytesIO(image_response.data)))  # type: ignore
        return result

    @translate_api_exceptions
    def get_fullres_image_urls(self, samples: SampleInfoList) -> Dict:
        """
        Retrieve the full resolution image paths for a given list of samples.

        Args:
            samples: An instance of the 'SampleInfoList' class that contains
            a list of samples.

        Returns:
            A dictionary that maps each point ID to its corresponding
            full resolution image path.

        Raises:
            ValueError: If the 'samples' input is empty or if the catalog \
                tag source response is empty.
        """
        points = [str(point) for point in samples.get_point_ids()]
        if len(points) == 0:
            raise UserError("Invalid input: No samples in the request")
        if not samples.job_id:
            raise UserError("Request ID cannot be empty")
        catalog_tag_resp: (
            CatalogTagSourceResponse
        ) = self.catalog_source_tag_api.fetch_catalog_db_tags(
            rid=samples.job_id,
            points=",".join(points),
        )  # type: ignore
        if (catalog_tag_resp.data is None) or len(catalog_tag_resp.data) == 0:
            raise ValueError("Empty response from server")
        point_tags = {}
        col_of_interest = "file_path"
        assert catalog_tag_resp.column_meta is not None
        for col_type in catalog_tag_resp.column_meta:
            if "file_path" in col_type.column_name:
                col_of_interest = col_type.column_name
                break

        for point_info in catalog_tag_resp.data:
            point_id = point_info.point_id
            for tag in point_info.tags:
                point_tags[point_id] = self._get_column_val(
                    tag, column_of_interest=[col_of_interest]
                ).get(col_of_interest)
        return point_tags

    def _get_column_val(
        self, tags: List[ColumnData], column_of_interest: List[str]
    ):
        tags_values = {}
        for tag in tags:
            if tag.column_name in column_of_interest:
                if tag.value:
                    tags_values[tag.column_name] = tag.value
        return tags_values

    def get_image_from_path(self, image_path) -> Image.Image:
        """
        Parameters
        ----------
        image_path : str
            The path to the image to retrieve.

        Returns
        -------
        Image
            The requested image.
        """
        image_path = image_path.replace("/ds/images/", "")
        api_response = self.image_fetch_api.fetch_image(image_path)
        img = Image.open(api_response)  # type: ignore
        return img

    @translate_api_exceptions
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
        if context == JobStatisticsContext.CONFUSION_MATRIX:
            return self.get_confusion_matrix(job, **kwargs)
        raise NotImplementedError()

    def get_confusion_matrix(self, job: Job, **kwargs) -> ConfusionMatrix:
        """
        Retrieves the confusion matrix from an analyze job.

        Parameters
        ----------
        job : Job
            The Job object to get the confusion matrix for.

        Returns
        -------
        ConfusionMatrix
            A confusion matrix object.
        """
        job_id = job.get_id()
        (
            default_score_thresh,
            default_iou_thresh,
        ) = self._get_default_score_iou_thresholds(job_id=job_id)
        iou_threshold = kwargs.get("iou_config_threshold", default_iou_thresh)
        score_threshold = kwargs.get(
            "confidence_score_threshold", default_score_thresh
        )

        api_response = self.request_stat_api.get_confusion_matrix(
            rid=job_id,
            score_threshold=score_threshold,
            iou_threshold=iou_threshold,
        )
        assert api_response is not None
        cells = api_response.data  # type: ignore
        class_names = np.unique([item.ground_truth_class for item in cells])
        num_classes = len(class_names)

        cm = np.zeros((num_classes, num_classes), dtype=np.int32)
        for i, j in np.ndindex(num_classes, num_classes):
            cm[i, j] = cells[i * num_classes + j].num_samples
        return ConfusionMatrix(cm, class_names)

    def get_confusion_matrix_cell(
        self, job: Job, true_label: str, predicted_label: str, **kwargs
    ) -> SampleInfoList:
        """
        Retrieves a cell from the confusion matrix of an analyze job.

        Parameters
        ----------
        job : Job
            The Job object to get the confusion matrix cell for.
        true_label: str
            The true label of the cell.
        predicted_label: str
            The predicted label of the cell.
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
        job_id = job.get_id()
        (
            default_score_thresh,
            default_iou_thresh,
        ) = self._get_default_score_iou_thresholds(job_id=job_id)

        iou_threshold = kwargs.get("iou_config_threshold", default_iou_thresh)
        score_threshold = kwargs.get(
            "confidence_score_threshold", default_score_thresh
        )

        api_response = self.request_stat_api.get_confusion_matrix_points(
            rid=job_id,
            score_threshold=score_threshold,
            iou_threshold=iou_threshold,
            prediction_class=predicted_label,
            ground_truth_class=true_label,
        )
        point_ids = api_response.points[0].points_ids  # type: ignore
        assert job_id is not None
        return SampleInfoList(job_id=job_id, point_ids=point_ids)

    def _get_default_score_iou_thresholds(self, job_id) -> Tuple[float, float]:
        resp: (
            dsp.AnalyzeMetaGetResponse
        ) = self.request_api.get_analyze_metadata(
            rid=job_id
        )  # type: ignore
        assert resp.confidence_config is not None
        iou_threshold = resp.iou_config.levels[0]  # type: ignore
        score_threshold = resp.confidence_config.levels[  # type: ignore
            len(resp.confidence_config.levels) // 2
        ]
        return score_threshold, iou_threshold

    def get_similar_samples(
        self,
        job: Job,
        positive_samples: List[str],
        negative_samples: List[str],
        max_count: int,
        timeout: int = 120,
    ) -> SampleInfoList:
        """
        Retrieves samples after performing a similarity search.

        Parameters
        ----------
        job : Job
            The Job object to get the confusion matrix cell for.
        positive_samples: List[str]
            The file paths of positive samples to use for similarity search.
        negative_samples: List[str]
            The file paths of negative samples to use for similarity search.
        max_count: int, optional
            The maximum number of samples to return.
        timeout: int, optional
            The maximum number of seconds to wait for similarity search
            to complete.

        Returns
        -------
        SampleInfoList
            A SampleInfoList object.
        """
        job_id = job.get_id()
        pos_point_ids = None
        neg_point_ids = None
        pos_points_list = []
        neg_points_list = []
        if positive_samples:
            pos_point_ids = self.get_samples_from_file_path(
                job, positive_samples
            )
        if negative_samples:
            neg_point_ids = self.get_samples_from_file_path(
                job, negative_samples
            )
        if pos_point_ids:
            pos_points_list = [
                {"point": point_id, "weight": 1}
                for point_id in pos_point_ids.values()
            ]
        if neg_point_ids:
            neg_points_list = [
                {"point": point_id, "weight": 0}
                for point_id in neg_point_ids.values()
            ]

        points_src = {"in_context": pos_points_list + neg_points_list}
        nclusters = job.info.tunables_default.nclusters  # type: ignore
        # FIXME : cluster map needs to be fixed
        cluster_map = {str(i): 0 for i in range(nclusters)}

        # initiate a similarity search
        create_sim_search_v2 = dsp.CreateSimSearchV2(
            n_neighbors=100,
            job_title="sim_search",
            search_space={
                "target": "universe",
                "tunables": {
                    "cluster-algo": "hdbscan",
                    "nclusters": nclusters,
                    "sample-mode": "outlier",
                    "sample-frac": 1,
                    "sample-weight": 2,
                    "cluster_map": cluster_map,
                },
            },
            tags=["sim_search_request_v2"],
            points_src=points_src,
        )

        search_response: (
            CreateSimSearchResponseV2
        ) = self.search_api.create_sim_search(
            rid=job_id,
            create_sim_search_v2=create_sim_search_v2,
        )  # type: ignore
        assert search_response
        sim_search_id = search_response.sim_search_rid
        assert sim_search_id
        # create a new scenario and execute
        scenario_name = "scenario" + sim_search_id
        search_configuration = {"distance_metric": "euclidean"}
        create_scenario_request = dsp.CreateScenarioRequest(
            name=scenario_name,
            init_dataset_id=job.dataset_id,  # type: ignore
            pipeline_id=job.pipeline_id,  # type: ignore
            is_top_level=False,
            search_configuration=search_configuration,
            source={
                "request": {
                    "request_id": job_id,
                    "sim_search_id": sim_search_id,
                }
            },
        )

        scenario_response = self.scenario_api.create_scenario(
            create_scenario_request=create_scenario_request,
        )
        scenario_id = scenario_response.scenario_id  # type: ignore
        create_scenario_execution = dsp.CreateScenarioExecution(
            search_configuration=search_configuration,
            search_target={"ds_request_id": job_id},
            scenario_id=scenario_id,
        )

        execution_response = self.scenario_exec_api.create_scenario_execution(
            create_scenario_execution=create_scenario_execution,
        )
        execution_id = execution_response.execution_id  # type: ignore

        # poll for execution progress
        ready = False
        while True:
            progress_response = self.scenario_exec_api.get_scenario_execution(
                execution_id
            )
            ready = progress_response.status == "READY"  # type: ignore
            if ready or timeout <= 0:
                break
            time.sleep(1)
            timeout -= 1

        samples = SampleInfoList()
        if ready:
            resultset_id = progress_response.resultset_id  # type: ignore
            attributes = {
                "request_id": job_id,
                "page_number": 1,
                "page_size": max_count,
            }
            api_response = self.resultset_api.get_resultset(
                resultset_id, **attributes
            )
            for sample in api_response.resultset.data[0].frames:  # type: ignore
                samples.append_sample(sample)

        # delete the newly created scenario
        self.scenario_api.delete_scenario(
            scenario_id,
        )
        if not ready:
            raise ServerError("Similarity search timed out")
        assert job_id is not None
        samples.job_id = job_id
        return samples

    @translate_api_exceptions
    def get_samples_from_file_path(
        self, job: Job, file_list: List[str], timeout: int = 120
    ) -> Dict:
        """_summary_

        Args:
            job (Job): Job object
            file_list (List[str]): List of files (file_path values)
            timeout: int, optional
            The maximum number of seconds to wait for catalog query
            to complete.

        Returns:
            Dict: dictionary of file_path to point_ids
        """
        job_id = job.get_id()
        assert job_id is not None

        ds_resp: GetDatasetRequestResponse = (
            self.request_api.get_request_details(job_id)
        )  # type: ignore
        file_path_col = "file_path"
        assert ds_resp.request_source_meta is not None
        for col_type in ds_resp.request_source_meta.column_type_map:
            if "file_path" in col_type["name"]:
                file_path_col = col_type["name"]
                break

        catalog_filter = CatalogSourceFilter(
            column_name=file_path_col,
            column_values=file_list,
            sql_operator="in",
        )

        request = CreateCatalogSourceRefine(
            case_sensitive=True,
            filter_description="",
            filters=[catalog_filter],
        )
        catalog_filter_resp: (
            RequestCatalogTagFilterSourceResp
        ) = self.catalog_source_tag_api.create_catalog_source_filter(
            rid=job_id, create_catalog_source_refine=request
        )  # type: ignore

        filter_id = catalog_filter_resp.catalog_filter_id

        # poll for execution progress
        while True:
            resp: (
                CatalogRefineResponse
            ) = self.catalog_source_tag_api.fetch_catalog_source_filter_info(
                # noqa: E501
                rid=job_id, catalog_filter_id=filter_id,
                request_plot=RequestPlot()
            )  # type: ignore
            if resp.status != CatalogFilterStatus.PROCESSING.value or timeout <= 0:
                break
            time.sleep(1)
            timeout -= 1

        if timeout <= 0:
            raise ServerError("Catalog Query timed out")

        if resp.status != CatalogFilterStatus.COMPLETE.value:
            raise ServerError("Catalog Query failed. Please Try again.")

        assert resp.points is not None
        res = dict(map(lambda i, j: (i, j), file_list, resp.points))
        return res

    @translate_api_exceptions
    def get_samples(
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
        Returns
        -------
        SampleInfoList
            A SampleInfoList object.
        """
        if job_context == JobContext.CONFUSION_MATRIX_CELL:
            return self.get_confusion_matrix_cell(
                job, spec["true_label"], spec["predicted_label"], **kwargs
            )
        if job_context == JobContext.SIMILARITY_SEARCH:
            max_count_val = spec["max_count"] if "max_count" in spec else 16
            timeout_val = spec["timeout"] if "timeout" in spec else 60
            return self.get_similar_samples(
                job,
                spec["positive_samples"],
                spec["negative_samples"],
                max_count_val,
                timeout_val,
            )
        if job_context == JobContext.CLUSTER_RETRIEVAL:
            max_count_val = spec["max_count"] if "max_count" in spec else 16
            cluster_id = spec["cluster_id"]
            return self.get_cluster_samples(job, cluster_id, max_count_val)
        if job_context == JobContext.CORESET_SAMPLING:
            percent = spec["percent"]
            return self.get_coreset_samples(job, percent)
        raise NotImplementedError()

    @translate_api_exceptions
    def get_job_display_panel_uri(self, job: Job) -> str:
        """
        Retrieves the job panel in the Data Explorer.

        Parameters
        ----------
        job : Job
            The Job object to be queried.
        width: int, Optional
            The width of the job panel in pixels
        height: int, Optional
            The height of the job panel in pixels

        Returns
        -------
        IFrame
            The job panel.
        """
        job_id = job.get_id()
        assert job_id is not None
        resp: GetDatasetRequestResponse = self.request_api.get_request_details(
            job_id
        )  # type: ignore

        uri = f"/#/datavis?view=main&job_type={resp.job_type}&job_id={job_id}"
        return uri

    def get_cluster_samples(
        self,
        job: Job,
        cluster_id: int,
        max_count: int = 16,
    ) -> SampleInfoList:
        """
        Retrieves samples for the specified cluster in a Job object.

        Parameters:
        -----------
        job : Job
            The job containing the cluster to retrieve the samples for.
        cluster_id : int
            The id of the cluster to retrieve the samples for.
        max_count : int
            The number of samples to retrieve.

        Returns:
        --------
        SampleInfoList
            A SampleInfoList object.
        """
        request_plot = dsp.RequestPlot(
            tunables={
                "cluster-algo": "hdbscan",
                "nclusters": 0,
                "sample-frac": 1,
                "sample-mode": "outlier",
                "sample-weight": 2,
            }
        )
        job_id = job.get_id()
        assert job_id is not None
        # TODO: request for max_count samples
        api_response = self.request_api.visualize_and_plot_request(
            rid=job_id, request_plot=request_plot
        )
        assert api_response is not None
        data = json.loads(api_response[1:])["data"]  # type: ignore
        point_ids = []
        for item in data:
            if item["cluster"] == cluster_id:
                point_ids.append(item["name"])
                if len(point_ids) >= max_count:
                    break
        return SampleInfoList(job_id=job_id, point_ids=point_ids)

    def get_coreset_samples(self, job: Job, percent: float) -> SampleInfoList:
        """
        Retrieves a coreset of a dataset.

        Parameters:
        -----------
        job : Job
            The Job object to be queried.
        percent: float
            The size of the desired coreset as a percentage of dataset size.

        Returns:
        --------
        SampleInfoList
            A SampleInfoList object.
        """
        sample_frac = percent / 100.0
        request_plot = dsp.RequestPlot(
            tunables={
                "nclusters": 0,
                "sample-frac": sample_frac,
                "sample-mode": "coreset",
                "sample-weight": 2,
            }
        )
        job_id = job.get_id()
        assert job_id is not None
        api_response = self.request_api.visualize_and_plot_request(
            rid=job_id, request_plot=request_plot
        )
        # exclude the prefix character
        assert api_response is not None
        data = json.loads(api_response[1:])["data"]  # type: ignore
        point_ids = [item["name"] for item in data]
        return SampleInfoList(job_id=job_id, point_ids=point_ids)

