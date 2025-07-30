"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""

from enum import Enum

import akridata_akrimanager_v2 as am
import akridata_dsp as dsp


class DatastoreType(Enum):
    """Supported datastore types"""

    LOCAL = 0
    S3 = 1
    AZURE = 2
    GCS = 3


class DataType(Enum):
    """Supported Data types"""

    IMAGE = "image/*"
    VIDEO = "video/*"


class JobType(dsp.JobType):
    """Supported Job types"""

    COMPARE = "COMPARE"

    @classmethod
    def is_analyze_job(cls, job_type) -> bool:
        if job_type in [
            cls.ANALYZE_CLASSIFICATION,
            cls.ANALYZE_OBJECT_DETECTION,
            cls.ANALYZE_SEGMENTATION,
        ]:
            return True
        return False


class FeaturizerType(Enum):
    """Type of featurizer to be used for ingestion
    FULL_IMAGE: Features generated on the full image
    PATCH: Features generated on a grid of cells over image. Supports patch
    search
    EXTERNAL: Features are generated externally and registered against dataset
    CLIP: OpenCLIP model trained on LAION dataset that generates features to
    allow text prompt based search.
    """

    FULL_IMAGE = "default"
    PATCH = "patch"
    EXTERNAL = "external"
    CLIP = "clip"


class ClusterAlgoType(str, Enum):
    """Cluster algorithms supported by DataExplorer"""

    HDBSCAN = "hdbscan"
    KMEANS = "kmeans"
    GMM = "gmm"
    KSEGMENT = "ksegment"


class EmbedAlgoType(str, Enum):
    """Embedding algorithms supported by DataExplorer"""

    UMAP = "umap"
    PCA = "pca"
    LLE = "lle"
    ISOMAP = "isomap"
    GEOMETRIC_CLASS = "geometric-class"


class JobContext(str, Enum):
    """Specifies the context that samples are requested under"""

    CONFUSION_MATRIX_CELL = "confusion_matrix"
    SIMILARITY_SEARCH = "similarity_search"
    CLUSTER_RETRIEVAL = "cluster_retrieval"
    CORESET_SAMPLING = "coreset_sampling"


class JobStatisticsContext(Enum):
    """Specifies the type of statistics to be retrieved"""

    CONFUSION_MATRIX = 0
    PRECISION_RECALL_CURVE = 1
    CONFIDENCE_HISTOGRAM = 2


class BackgroundTaskType(Enum):
    """Specifies the type of background task"""

    DATASET_INGESTION = "dataset_ingestion"


class CatalogTableType(Enum):
    """TableType for create view"""

    INTERNAL = am.TableType.INTERNAL
    EXTERNAL = am.TableType.EXTERNAL


class DockerImageType(object):
    """Docker Image Type for Docker Image"""

    FEATURIZER = "featurizer"


class AkridataDockerNames(object):
    """Akridata Default Docker Names"""

    AKRIDATA_IMAGE_PREPROCESSOR = "AkridataImagePreprocessor"
    AKRIDATA_THUMBNAIL_GENERATOR = "AkridataThumbnail"


class SqlTypes(str, Enum):
    """Catalog Table SQL Types"""

    BIGINT = "BIGINT"
    INT = "INT"
    FLOAT = "FLOAT"
    DOUBLE = "DOUBLE"
    DATETIME = "DATETIME"
    TIME = "TIME"
    VARCHAR = "VARCHAR([N])"


class OutputPortType(str, Enum):
    """Possible output port type for featurizer"""

    full = "full"
    patch = "patch"
