from enum import Enum


class TableNames(Enum):
    PRIMARY = "primary"
    BLOB = "blob"
    SUMMARY = "summary"
    PARTITIONER_FILES = "partitioned_files"
    DATASET_FILES = "dataset_files"
