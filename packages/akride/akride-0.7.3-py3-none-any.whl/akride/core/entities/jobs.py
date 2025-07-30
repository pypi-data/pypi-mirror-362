"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""
from typing import Dict, Union

import akridata_dsp as dsp

from akride.core.entities.datasets import Dataset
from akride.core.entities.entity import Entity
from akride.core.types import AnalyzeJobParams, CatalogTable, PlotFeaturizer

from akride.core.enums import (  # isort:skip
    ClusterAlgoType,
    EmbedAlgoType,
    JobType,
)


class JobSpec(Dict):
    """
    Class representing a job specification.
    TODO: separate specs for different job types
    """

    def __init__(self, dataset: Dataset, **kwargs):
        """
        Constructor for the JobSpec class.

        Parameters:
        -----------
        dataset: Dataset
            The dataset to explore.
        job_type : str
            The job type - 'EXPLORE', 'ANALYZE' etc.
        job_name : str, optional
            The name of the job to create. A unique name will be generated if
            this is not given.
        predictions_file: str, optional
            The path to the catalog file containing predictions and ground
            truth.
            This file must be formatted according to the specification at:
            https://docs.akridata.ai/docs/analyze-job-creation-and-visualization
        cluster_algo : ClusterAlgoType, optional
            The clustering algorithm to use.
        embed_algo : EmbedAlgoType, optional
            The embedding algorithm to use.
        num_clusters : int, optional
            The number of clusters to create.
        pipeline: Pipeline
            Pipeline information
        max_images : int, optional
            The maximum number of images to use.
        catalog_table : CatalogTable, optional
            The catalog to be used for creating this explore job. This defaults
            to the internal primary catalog that is created automatically when
            a dataset is created.
        filters : List[Condition], optional
            The filters to be used to select a subset of examples for this job.
            These filters are applied to the catalog specified by catalog_name.
        analyze_params: AnalyzeParams, optional
            Additional params for Analyze job
        is_compare: bool, optional
            Whether this is a compare job
        reference_job: Job, optional
            The reference job for this compare job
        """
        defaults = {
            "dataset": dataset,
            "job_type": JobType.EXPLORE,
            "predictions_file": "",
            "job_name": "",
            "cluster_algo": ClusterAlgoType.HDBSCAN,
            "embed_algo": EmbedAlgoType.UMAP,
            "num_clusters": None,
            "max_images": 1000,
            "catalog_table": CatalogTable(table_name="primary"),
            "filters": None,
            "analyze_params": None,
            "pipeline": None,
        }

        super().__init__()
        self.update(defaults)
        self.update(kwargs)
        if not self["job_name"]:
            # TODO: generate a unique name
            self["job_name"] = "DEFAULT-JOB-NAME"
        if (
            JobType.is_analyze_job(job_type=self["job_type"])
            and self["analyze_params"] is not None
        ):
            params: AnalyzeJobParams = self["analyze_params"]
            if self["job_type"] == JobType.ANALYZE_CLASSIFICATION:
                params.plot_featurizer = PlotFeaturizer.LABEL
            if (
                self["job_type"] == JobType.ANALYZE_SEGMENTATION
                or self["job_type"] == JobType.ANALYZE_OBJECT_DETECTION
            ):
                params.plot_featurizer = PlotFeaturizer.CONTENT
        if self["pipeline"] is None:
            raise ValueError("Pipeline is not specified")

        if self["is_compare"] and not self["reference_job"]:
            raise ValueError("Reference job is required to create compare job")


class Job(Entity):
    """
    Class representing a job entity.
    """

    def __init__(
        self, info: Union[dsp.CreateJobRequestResponse, dsp.CompatibleRefJob]
    ):
        """
        Constructor for the Job class.

        Parameters
        ----------
        info : dsp.models.dataset_job_request.DatasetJobRequest
            The job request object.
        """
        super().__init__("", "")
        self.info = info

    def delete(self) -> None:
        """
        Deletes an entity.

        Parameters
        ----------

        Returns
        -------
        None
        """
        return None

    @property
    def dataset_id(self):
        return self.info.dataset_id  # type: ignore

    @property
    def pipeline_id(self):
        return self.info.pipeline_id  # type: ignore

    def get_num_clusters(self) -> int:
        """Get the default number of clusters available for visualization

        :raises ValueError: If job details are not available
        :return: int
        """
        if self.info:
            return self.info.to_dict()["tunables_default"]["nclusters"]
        raise ValueError("job details are not unavailable")

    def get_max_clusters(self) -> int:
        """Get total number of clusters available for visualization

        :raises ValueError: If job details are not available
        :return: int
        """
        if self.info:
            return self.info.to_dict()["tunables_default"]["max_clusters"]
        raise ValueError("job details are not unavailable")

    @property
    def ownername(self):
        return self.info.ownername
