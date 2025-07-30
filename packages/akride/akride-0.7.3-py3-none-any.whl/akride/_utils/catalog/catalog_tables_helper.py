import re
from typing import Dict, List, Optional, Set

import akridata_akrimanager_v2 as am

from akride._utils.catalog.dataset_tables_info import DatasetTablesInfo
from akride._utils.catalog.pipeline_tables_info import PipelineTablesInfo
from akride.core.enums import SqlTypes
from akride.core.exceptions import UserError


class CatalogTablesHelper:
    VARCHAR_PATTERN = re.compile(r"VARCHAR\([1-9]\d*\)")

    def __init__(self, catalog_tables_resp: am.CatalogTableResponse):
        self._dataset_tables_info = DatasetTablesInfo(
            dataset_tables=catalog_tables_resp.dataset_tables
        )

        self._pipelines_table_info = [
            PipelineTablesInfo(pipeline_table=pipeline)
            for pipeline in catalog_tables_resp.pipelines
        ]

    def get_pipeline_tables_info(
        self, pipeline_ids: Optional[Set[str]] = None
    ) -> List[PipelineTablesInfo]:
        if not pipeline_ids:
            return self._pipelines_table_info

        return list(
            filter(
                lambda table: table.get_pipeline_id() in pipeline_ids,
                self._pipelines_table_info,
            )
        )

    def get_dataset_tables_info(self) -> DatasetTablesInfo:
        return self._dataset_tables_info

    @staticmethod
    def validate_and_create_sql_type_mapping(
        schema: Dict[str, str]
    ) -> List[Dict[str, str]]:
        sql_mappings = []

        valid_types = [val.value for val in SqlTypes]

        for col_name, col_type in schema.items():
            match = CatalogTablesHelper.VARCHAR_PATTERN.fullmatch(col_type)

            if match or col_type in valid_types:
                sql_mappings.append({"name": col_name, "type": col_type})

            else:
                raise UserError(
                    message=f"Invalid SQL type '{col_type}' "
                    f"for column '{col_name}'. "
                    f"Valid types are: {valid_types}"
                )

        return sql_mappings
