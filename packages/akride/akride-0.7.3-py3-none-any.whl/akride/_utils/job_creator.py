"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""

import time
from typing import List, Optional, Tuple

import akridata_akrimanager_v2 as am
import akridata_dsp as dsp
from akridata_akrimanager_v2 import (
    CatalogPipelineTable,
    CatalogTableResponse,
    MakeQueryTableRequest,
    QueryIdResponse,
    QueryResponse,
    Table,
)
from akridata_dsp import (
    CreateJobRequest,
    CreateJobRequestResponse,
    CreateSubmitJobRequest,
    DatasetInfo,
    EmbedderQuality,
    RequestDataSourceCreate,
    RequestSourceMetaJobRequestCreate,
    SubmitRequestTunables,
)

from akride.core.entities.jobs import Job
from akride.core.enums import ClusterAlgoType, EmbedAlgoType, JobType
from akride.core.exceptions import UserError
from akride.core.types import AnalyzeJobParams, CatalogDetails, CatalogTable


class JobCreator:  # pylint: disable=too-few-public-methods
    """Create a ds job"""

    def __init__(
        self,
        job_req_api: dsp.JobRequestsApi,
        qms_api: am.QueriesApi,
        catalog_api: am.CatalogApi,
        views_api: am.ViewsApi,
        request_api: dsp.RequestApi,
    ) -> None:
        self.job_req_api: dsp.JobRequestsApi = job_req_api
        self.request_api: dsp.RequestApi = request_api
        self.qms_api = qms_api
        self.catalog_api = catalog_api
        self.views_api: am.ViewsApi = views_api

    def create_job(  # pylint: disable=too-many-arguments
        self,
        job_type: JobType,
        job_name: str,
        dataset_id: str,
        clusterer_algo: str,
        embedder_algo: str,
        catalog_table: CatalogTable,
        pipeline_id: str,
        embedder_quality: str = EmbedderQuality.HIGH,
        cluster_first: bool = False,
        max_images: int = 1000,
        num_clusters: Optional[int] = None,
        analyze_params: Optional[AnalyzeJobParams] = None,
        is_compare: bool = False,
        reference_job: Job = None,
        filters: Optional[List[am.Condition]] = None,
    ) -> Tuple[CreateJobRequest, CreateJobRequestResponse]:
        """_summary_

        Args:
            job_type (str): Job Type
            job_name (str): Name of the Job
            dataset_id (str): Dataset ID
            clusterer_algo (ClusterAlgorithms): Clusterer algorithm
            embedder_algo (EmbeddingAlgorithms): Embedder algorithm
            pipeline_id (str, optional): Pipeline ID to use. Defaults to "".
            embedder_quality (str, optional): Embedder Quality. Defaults to
                EmbedderQuality.HIGH.
            cluster_first (bool, optional): If true clustering is done before
            embedding. Defaults to True.
            table_name (str, optional): Catalog table name. Defaults to "primary".
            max_images (int, optional): Max Images to use in the job. Defaults to 1000.
            num_clusters (Optional[int], optional): Number of clusters to
            create. Defaults to None.
            analyze_params: AnalyzeParams, optional
            is_compare: bool, optional: True if it is a compare job
            reference_job: reference job details
            Additional params for Analyze job

        Raises:
            ValueError: Invalid input

        Returns:
            Tuple[CreateJobRequest, CreateJobRequestResponse]: request and response
        """
        catalog_tables: CatalogTableResponse = (
            self.catalog_api.get_catalog_tables(dataset_id=dataset_id)
        )  # type: ignore

        required_pipeline: CatalogPipelineTable = self._find_required_pipeline(
            catalog_tables, pipeline_id=pipeline_id
        )
        if catalog_table.is_view:
            view_details = self.find_required_view(
                dataset_id=dataset_id, catalog_table=catalog_table
            )
            query_id = self._execute_view_query(
                view_id=view_details.view_id,  # type: ignore
                view_name=view_details.view_name,  # type: ignore
                limit=max_images,
                filters=filters,
            )
        else:
            req_table: Table = self._find_required_table(
                pipeline_info=required_pipeline, catalog_table=catalog_table
            )
            if not req_table.visualizable:
                raise ValueError(
                    f"table {catalog_table.table_name} is not visualizable"
                )
            if req_table.is_busy:
                raise ValueError(
                    f"table {catalog_table.table_name} is not ready for query yet..."
                    " Try again after sometime"
                )
            query_id: str = self._execute_table_query(
                dataset_id=dataset_id,
                pipeline_id=pipeline_id,
                table=req_table,
                limit=max_images,
            )
        self._wait_query_completion(query_id=query_id)
        request = self._get_job_request(
            job_name=job_name,
            dataset_id=dataset_id,
            pipeline_id=pipeline_id,
            query_id=query_id,
            job_type=job_type,
            clusterer_algo=clusterer_algo,
            embedder_algo=embedder_algo,
            embedder_quality=embedder_quality,
            cluster_first=cluster_first,
            num_clusters=num_clusters,
            analyze_params=analyze_params,
            is_compare=is_compare,
            reference_job=reference_job,
        )
        resp = self.request_api.create_job_request(
            create_job_request=request
        )  # type: ignore
        return request, resp  # type: ignore

    def _get_job_request(  # pylint: disable=too-many-arguments
        self,
        job_name: str,
        dataset_id: str,
        pipeline_id: str,
        job_type: JobType,
        query_id: str,
        clusterer_algo: str,
        embedder_algo: str,
        embedder_quality: str,
        cluster_first: bool,
        num_clusters: Optional[int] = None,
        analyze_params: Optional[AnalyzeJobParams] = None,
        is_compare: bool = False,
        reference_job: Job = None,
    ) -> CreateJobRequest:
        ds_req = DatasetInfo(dataset_id=dataset_id, pipeline_id=pipeline_id)
        req_data = RequestDataSourceCreate(catalog_filters=True)
        req_meta = RequestSourceMetaJobRequestCreate(vcs_query_id=query_id)
        submit_params = self._get_submit_params(
            job_type=job_type,
            clusterer_algo=clusterer_algo,
            embedder_algo=embedder_algo,
            embedder_quality=embedder_quality,
            cluster_first=cluster_first,
            num_clusters=num_clusters,
            analyze_params=analyze_params,
            is_compare=is_compare,
            reference_job=reference_job,
        )
        request = CreateJobRequest(
            dataset=ds_req,
            reqname=job_name,
            request_source_meta=req_meta,
            src=req_data,
            submit_params=submit_params,
        )
        return request

    def _get_submit_params(  # pylint: disable=too-many-arguments
        self,
        job_type: JobType = JobType.EXPLORE,
        clusterer_algo: str = ClusterAlgoType.HDBSCAN,
        embedder_algo: str = EmbedAlgoType.UMAP,
        embedder_quality: str = EmbedderQuality.HIGH,
        cluster_first: bool = True,
        num_clusters: Optional[int] = None,
        analyze_params: Optional[AnalyzeJobParams] = None,
        is_compare: bool = False,
        reference_job: Job = None,
    ) -> CreateSubmitJobRequest:
        tunables = None
        if not is_compare:
            tunables = SubmitRequestTunables(
                cluster_algo=clusterer_algo,
                cluster_first=cluster_first,
                embedder_algo=embedder_algo,
                embedder_quality=embedder_quality,
                nclusters=num_clusters,
            )
        datasource = None
        if JobType.is_analyze_job(job_type=job_type):
            catalog_db: dsp.CatalogDbAnalyzeMetaData = dsp.CatalogDbAnalyzeMetaData(
                field_columns=self._get_analyze_field_column_map(
                    az_config=analyze_params.catalog_config  # type: ignore
                )
            )
            if analyze_params is None or analyze_params.catalog_config is None:
                raise UserError("AnalyzeParams.catalog_config cannot be None")

            datasource: dsp.DataSourceSubmitRequest = (
                dsp.DataSourceSubmitRequest(
                    analyze=dsp.AnalyseSubmitRequest(
                        catalog_db=catalog_db,
                        confidence_config=dsp.AnalyzeMetaConfigItemRequest(
                            levels=analyze_params.confidence_config
                        ),
                        iou_config=dsp.AnalyzeMetaConfigItemRequest(
                            levels=analyze_params.iou_config
                        ),
                        plot_featurizer=analyze_params.plot_featurizer,
                    )
                )
            )

        src = None
        request_source_meta = None

        if is_compare:
            src: dsp.RequestDataSourceSubmit = dsp.RequestDataSourceSubmit(
                compare=True
            )
            request_source_meta: dsp.RequestSourceMetaJobRequestSubmit = (
                dsp.RequestSourceMetaJobRequestSubmit(
                    compare=dsp.CompareSourceMeta(
                        ref_request_id=reference_job.get_id(),
                        ref_request_owner=reference_job.ownername,
                    )
                )
            )
        return CreateSubmitJobRequest(
            job_type=job_type,
            tunables=tunables,
            data_source=datasource,
            src=src,
            request_source_meta=request_source_meta,
        )

    def _wait_query_completion(self, query_id: str):
        query_resp: QueryResponse = None  # type: ignore
        retries = 0
        while True:
            query_resp = self.qms_api.get_query(
                query_id=query_id,
            )  # type: ignore
            if (
                not query_resp
                or query_resp.status in ["COMPLETED", "FAILED"]
                or retries >= 60
            ):
                break
            time.sleep(1)
            retries = retries + 1
        if not query_resp or query_resp.status != "COMPLETED":
            raise ValueError(
                f"Unable to execute query: Query status: {query_resp.status}"
            )

    def _find_required_pipeline(
        self, catalog_tables: CatalogTableResponse, pipeline_id: str
    ) -> CatalogPipelineTable:
        required_pipeline: Optional[CatalogPipelineTable] = None
        assert catalog_tables.pipelines is not None
        pipeline: CatalogPipelineTable
        for pipeline in catalog_tables.pipelines:
            if pipeline.pipeline_id == pipeline_id:
                required_pipeline = pipeline
        if required_pipeline is None:
            raise ValueError(f"pipeline {pipeline_id} not found")
        return required_pipeline

    def find_required_view(
        self, dataset_id, catalog_table: CatalogTable
    ) -> am.ViewResponse:
        all_views: am.ListViewsResponse = self.views_api.list_views(
            dataset_id=dataset_id
        )  # type: ignore
        view_of_interest = [
            record
            for record in all_views.records  # type: ignore
            if record.view_name == catalog_table.table_name
        ]
        if not view_of_interest:
            raise UserError(f"Cannot find view {catalog_table.table_name}")
        return view_of_interest[0]

    def _find_required_table(
        self, pipeline_info: CatalogPipelineTable, catalog_table: CatalogTable
    ) -> Table:
        table: Table
        required_table: Optional[Table] = None
        assert pipeline_info.tables is not None
        for table in pipeline_info.tables:
            if table.name == catalog_table.table_name:
                required_table = table
                break
        if required_table is None:
            raise ValueError(f"table {catalog_table.table_name} not found")
        return required_table

    def _get_query_table_request(
        self, dataset_id: str, pipeline_id: str, table: Table, limit: int
    ) -> MakeQueryTableRequest:
        request = MakeQueryTableRequest(
            dataset_id=dataset_id,
            pipeline_id=pipeline_id,
            table_name=table.name,
            abs_table_name=table.abs_name,
            limit=limit,
        )
        return request

    def _execute_table_query(
        self,
        dataset_id: str,
        pipeline_id: str,
        table: Table,
        limit: int = 1000,
    ) -> str:
        request = self._get_query_table_request(
            dataset_id, pipeline_id=pipeline_id, table=table, limit=limit
        )
        query_id_response: QueryIdResponse = self.qms_api.make_query_table(
            make_query_table_request=request,
        )  # type: ignore

        assert query_id_response.query_id is not None
        return query_id_response.query_id

    def _execute_view_query(
        self,
        view_id: str,
        view_name: str,
        limit: int = 1000,
        filters: Optional[List[am.Condition]] = None,
    ) -> str:
        where_condition = (
            am.WhereCondition(query_conditions=filters) if filters else None
        )
        request: am.MakeQueryViewRequest = am.MakeQueryViewRequest(
            view_id=view_id,
            view_name=view_name,
            limit=limit,
            where_conditions=where_condition,
        )
        query_id_response: QueryIdResponse = self.qms_api.make_query_view(
            make_query_view_request=request
        )  # type: ignore

        assert query_id_response.query_id is not None
        return query_id_response.query_id

    def _get_analyze_field_column_map(self, az_config: CatalogDetails):
        return dsp.FieldColumnsCatalogDBMap(
            ground_truth_class=az_config.ground_truth_class_column,
            prediction_class=az_config.prediction_class_column,
            ground_truth_coords=az_config.ground_truth_coordinates_column,
            score=az_config.score_column,
            ground_truth_coords_class=az_config.ground_truth_coordinates_class_column,
            prediction_coords=az_config.prediction_coordinates_column,
            prediction_coords_class_score=az_config.prediction_coordinates_class_score_column,  # noqa: E501
        )

