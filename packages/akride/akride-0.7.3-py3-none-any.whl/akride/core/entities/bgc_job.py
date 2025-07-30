"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""

import akridata_akrimanager_v2 as am

from akride.core.entities.entity import Entity


class BGCJob(Entity):
    """
    Class representing a dataset entity.
    """

    def __init__(self, info: am.BCJobDetailedStatus):
        """
        Constructor for the Dataset class.
        """
        super().__init__(info.job_id)

        self.info = info

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
