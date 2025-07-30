from typing import List

import akridata_akrimanager_v2 as am

from akride._utils.catalog.enums import TableNames
from akride._utils.catalog.tables_info import TablesInfo


class DatasetTablesInfo(TablesInfo):
    def __init__(self, dataset_tables: List[am.Table]):
        super().__init__(tables=dataset_tables)

    def get_dataset_abs_table(self):
        return self.get_abs_table(table_name=TableNames.DATASET_FILES.value)

    def get_partitioned_abs_table(self):
        return self.get_abs_table(
            table_name=TableNames.PARTITIONER_FILES.value
        )
