import os

import akridata_akrimanager_v2 as am


class Constants:
    AKRIDE_TMP_DIR = os.path.join("/", "tmp", ".akride")

    DEFAULT_IMAGE_BLOB_EXPR = "*(png|jpg|gif|jpeg|tiff|tif|bmp)"
    DEFAULT_VIDEO_BLOB_EXPR = "*(mov|mp4|avi|wmv|mpg|mpeg|mkv)"

    LOG_CONFIG_FILE_NAME = "pylogconf.yaml"

    DEFAULT_SAAS_ENDPOINT = "https://app.akridata.ai"

    PARTITION_TIME_FRAME = 300000000

    INGEST_IMAGE_WF_TOKEN_SIZE = 1024
    INGEST_IMAGE_PARTITION_SIZE = 10000
    PROCESS_IMAGE_WF_TOKEN_SIZE = 1500

    # Only 1 video per token is supported.
    # DO NOT MODIFY THIS VALUE
    INGEST_VIDEO_PARTITION_SIZE = 10
    INGEST_VIDEO_WF_TOKEN_SIZE = 1
    PROCESS_VIDEO_WF_TOKEN_SIZE = 1
    VIDEO_CHUNK_SIZE = 300

    THUMBNAIL_AGGREGATOR_SDK_DETAILS = am.AkriSDKFilterDetails(
        run_method="run",
        module="pyakri_de_filters.thumbnail.thumbnail_aggregator",
        class_name="ThumbnailAggregator",
    )
    DATASET_FILES_COLUMNS = [
        "partition_start",
        "partition_end",
        "workflow_id",
        "session_id",
        "file_path",
    ]
    PARTITIONED_TABLE_COLUMNS = [
        "partition_start",
        "partition_end",
        "workflow_id",
        "session_id",
        "file_path",
        "file_id",
        "partition_id",
    ]

    DEBUGGING_ENABLED = os.getenv("ENABLE_DEBUG_LOGS", "").lower() == "true"

    IMPORT_CATALOG_STATUS_CHECK_INTERVAL_S = 10
    IMPORT_CATALOG_STATUS_CHECK_ATTEMPTS = 50
    DEFAULT_FEATURE_VALUE = "1"
