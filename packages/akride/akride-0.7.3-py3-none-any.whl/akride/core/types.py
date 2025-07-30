"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""


import pprint
from dataclasses import dataclass
from typing import Dict, List, Optional

import akridata_dsp as dsp
from akridata_akrimanager_v2 import ApiClient as AMApiClient
from akridata_dsp import ApiClient as DSPApiClient
from attr import define, field

from akride.background_task_manager import BackgroundTaskManager
from akride.core.enums import CatalogTableType


@dataclass
class ClientManager:
    """Dataclass managing different APIClient required to connect
    with DataExplorer services
    """

    am_client: AMApiClient
    dsp_client: DSPApiClient
    background_task_manager: BackgroundTaskManager


class JobStatistics:
    def __init__(self):
        pass


class ConfusionMatrix(JobStatistics):
    """
    Class representing a confusion matrix.
    """

    def __init__(self, data, labels):
        """
        Constructor for the ConfusionMatrix class.

        Parameters
        ----------
        data : numpy.ndarray of shape (n_classes, n_classes)
            The confusion matrix with true labels as the vertical axis
            and predicted labels as the horizontal axis.
        labels : List[str]
            The names of labels in alphabetical order.
        """
        self.data = data
        self.labels = labels

    def to_dict(self) -> dict:
        """
        Method for converting this object to a dictionary.

        Returns
        -------
        dict
            A dictionary representing this object.
        """
        return vars(self)

    def __repr__(self) -> str:
        """
        Method for representing this object as a string.

        Returns
        -------
        str
            A formatted string representing this object.
        """
        return pprint.pformat(self.to_dict())


class JobOpSpec(Dict):
    def __init__(self, **kwargs):
        pass


class ConfusionMatrixCellSpec(JobOpSpec):
    """
    Class representing a confusion matrix cell specification.
    """

    def __init__(self, **kwargs):
        """
        Constructor for the ConfusionMatrixCellSpec class.

        Parameters:
        -----------
        true_label: str, optional
            The true label of the confusion matrix cell.
        predicted_label: str, optional
            The predicted label of the confusion matrix cell.
        """
        super().__init__()
        self.update(kwargs)


class SimilaritySearchSpec(JobOpSpec):
    """
    Class representing a similarity search specification.
    """

    def __init__(self, **kwargs):
        """
        Constructor for the SimilaritySearchSpec class.

        Parameters:
        -----------
        positive_samples: List[str], optional
            The file paths of positive samples to use for
            similarity search.
        negative_samples: List[str], optional
            The file paths of negative samples to use for
            similarity search.
        max_count: int, optional
            The maximum number of samples to return.
        timeout: int, optional
            The maximum number of seconds to wait for similarity search
            to complete.
        """
        defaults = {
            "max_count": 16,
            "timeout": 60,
        }

        super().__init__()
        self.update(defaults)
        self.update(kwargs)


class ClusterRetrievalSpec(JobOpSpec):
    """
    Class representing a cluster retrieval specification.
    """

    def __init__(self, **kwargs):
        """
        Constructor for the ClusterRetrievalSpec class.

        Parameters:
        -----------
        cluster_id: int
            The ID of the cluster to retrieve samples from
        max_count: int, optional
            The maximum number of samples to return.
        """
        defaults = {
            "max_count": 16,
        }

        super().__init__()
        self.update(defaults)
        self.update(kwargs)


class CoresetSamplingSpec(JobOpSpec):
    """
    Class representing a coreset sampling specification.
    """

    def __init__(self, **kwargs):
        """
        Constructor for the CoresetSamplingSpec class.

        Parameters:
        -----------
        percent: float, optional
            The size of the desired coreset as a percentage of dataset size.
        """
        defaults = {
            "percent": 10,
        }

        super().__init__()
        self.update(defaults)
        self.update(kwargs)


class SampleInfoList:
    """
    Class representing a list of samples.
    """

    def __init__(self, job_id: str = "", point_ids: Optional[List] = None):
        """
        Constructor for the SampleInfoList class.

        Parameters
        ----------
        job_id: str
            The ID of the associated job.
        point_ids: List, optional
            The indices of the samples in this list.
        """
        self.point_ids = point_ids if point_ids else []
        self._data = []
        self.job_id = job_id

    def append_sample(
        self,
        sample: dsp.ResultsetResponseFrameItem,
    ):
        # delete "file:" prefix from path
        assert sample.file_path is not None
        file_path = sample.file_path[5:]
        self.point_ids.append(sample.point_id)
        self._data.append(
            (file_path, sample.high_res_url, sample.point_id, sample.url)
        )

    def get_local_paths(self):
        return [item[0] for item in self._data]

    def get_fullres_urls(self):
        return [item[1] for item in self._data]

    def get_point_ids(self):
        if not self.point_ids and self._data:
            return [item[2] for item in self._data]
        return self.point_ids

    def get_thumbnail_urls(self):
        return [item[3] for item in self._data]

    def to_dict(self) -> dict:
        """
        Method for converting this object to a dictionary.

        Returns
        -------
        dict
            A dictionary representing the this object.
        """
        return vars(self)

    def __repr__(self) -> str:
        """
        Method for representing this object as a string.

        Returns
        -------
        str
            A formatted string representing this object.
        """
        return pprint.pformat(self.to_dict())

    def __len__(self) -> int:
        if self._data:
            return len(self._data)
        return len(self.point_ids)

    def __getitem__(self, key):
        if isinstance(key, slice):
            result = SampleInfoList()
            result.point_ids = self.point_ids[key]
            if self._data:
                result._data = self._data[key]
            result.job_id = self.job_id
            return result
        if isinstance(key, int):
            return self._data[key]
        raise TypeError(f"Invalid key type {type(key)}")


class CatalogTable(object):
    def __init__(
        self,
        table_name: str,
        table_type: Optional[CatalogTableType] = None,
        pipeline_id: Optional[str] = None,
        catalog_name: Optional[str] = None,
        schema_name: Optional[str] = None,
        alias_name: Optional[str] = None,
        is_view: Optional[bool] = False,
    ):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class with all of its attributes and methods.


        :param table_name: str: Set the table_name attribute of the class
        :param table_type: Table: Set the table type for the table
        (INTERNAL/EXTERNAL) using the akride.TableType
        :param pipeline_id: str: Identify the pipeline
        :param is_view: bool:  Whether the table in question is a view
        :return: instance of this class
        """
        self.table_name = table_name
        self.pipeline_id = pipeline_id
        self.table_type: CatalogTableType = (
            table_type if table_type else CatalogTableType.INTERNAL
        )
        self.catalog_name = catalog_name
        self.schema_name = schema_name
        self.alias_name = (
            alias_name if alias_name is not None else f"{self.table_name}_1"
        )
        self.is_view = is_view


class PlotFeaturizer(dsp.PlotFeaturizer):
    """PlotFeaturizer for Analyze job"""


class JoinCondition(object):
    def __init__(self, left_column, right_column):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines what attributes it has.


        :param left_column:str left column name
        :param right_column:str right column name
        :return: The instance of the class
        """
        self.left_column = left_column
        self.right_column: str = right_column


@define
class CatalogDetails(object):
    score_column: str = field(default=None)
    ground_truth_class_column: str = field(default=None)
    prediction_class_column: str = field(default=None)
    ground_truth_coordinates_column: str = field(default=None)
    prediction_coordinates_column: str = field(default=None)
    ground_truth_coordinates_class_column: str = field(default=None)
    prediction_coordinates_class_score_column: str = field(default=None)


@define
class Column(object):
    """Type representing a Table Column"""

    name: str
    type: str


@define
class AnalyzeJobParams(object):
    catalog_config: CatalogDetails
    plot_featurizer: str = PlotFeaturizer.CONTENT
    confidence_config: List[float] = [0, 0.2, 0.4, 0.6, 0.8, 1]
    iou_config: List[float] = [0.1, 0.3, 0.5, 0.7, 0.9, 1]
