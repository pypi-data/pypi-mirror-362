from typing import List

import akridata_akrimanager_v2 as am


class TablesInfo:
    def __init__(self, tables: List[am.Table]):
        self.tables = tables
        self.tables_map = {}
        self.populate_tables_map()

    def populate_tables_map(self):
        for table in self.tables:
            self.tables_map[table.name] = table.abs_name

    def get_abs_table(self, table_name):
        if table_name in self.tables_map:
            return self.tables_map[table_name]

        raise ValueError(f"Table {table_name} not found!")
