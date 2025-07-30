import akridata_akrimanager_v2 as am

from akride._utils.catalog.enums import TableNames
from akride._utils.catalog.tables_info import TablesInfo


class PipelineTablesInfo(TablesInfo):
    def __init__(self, pipeline_table: am.CatalogPipelineTable):
        super().__init__(tables=pipeline_table.tables)
        self._pipeline_name = pipeline_table.pipeline_name
        self._pipeline_id = pipeline_table.pipeline_id

    def get_primary_abs_table(self):
        return self.get_abs_table(table_name=TableNames.PRIMARY.value)

    def get_summary_abs_table(self):
        return self.get_abs_table(table_name=TableNames.SUMMARY.value)

    def get_blobs_abs_table(self):
        return self.get_abs_table(table_name=TableNames.BLOB.value)

    def get_pipeline_name(self) -> str:
        return self._pipeline_name

    def get_pipeline_id(self) -> str:
        return self._pipeline_id
