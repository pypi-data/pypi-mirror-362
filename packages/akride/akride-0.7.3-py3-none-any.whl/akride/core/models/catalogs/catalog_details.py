from dataclasses import dataclass


@dataclass
class CatalogDetails:
    """
    Class representing parameters details for creating a catalog.

    Attributes:
        table_name : str
            The name of the table to create for the catalog.
        catalog_csv_file : str
            The path to the CSV file containing new catalog data.
    """

    table_name: str
    catalog_csv_file: str
