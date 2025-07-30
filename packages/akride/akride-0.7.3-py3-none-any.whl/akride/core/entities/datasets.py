"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""

import akridata_akrimanager_v2 as am

from akride.core.entities.entity import Entity


class Dataset(Entity):
    """
    Class representing a dataset entity.
    """

    def __init__(self, info: am.DataSetsItem):
        """
        Constructor for the Dataset class.
        """
        super().__init__(info.id, info.name)
        self.info = info
        self.id = info.id
        self.name = info.name

    def delete(self) -> None:
        """
        Deletes an entity.

        Parameters
        ----------

        Returns
        -------
        None
        """
        return None
