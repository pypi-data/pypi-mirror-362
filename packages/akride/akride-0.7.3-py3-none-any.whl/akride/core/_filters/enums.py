from enum import Enum


class FilterTypes(Enum):
    Partitioner = "partitioner"
    Preprocessor = "preprocessor"
    Featurizer = "featurizer"
    DataIngest = "data_ingest"
    Thumbnail = "thumbnail"
    ThumbnailAggregator = "thumbnail_aggregator"
