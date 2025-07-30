from dataclasses import dataclass


@dataclass
class CatalogViewInfo:
    """
    Class representing the details of View.

    Attributes:
        view_id : str
            The id associated to view

    """

    view_id: str
