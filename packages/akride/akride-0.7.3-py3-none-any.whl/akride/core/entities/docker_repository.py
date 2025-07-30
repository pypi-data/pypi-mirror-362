"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""

import akridata_akrimanager_v2 as am

from akride.core.entities.entity import Entity


class DockerRepository(Entity):
    """
    Class representing a Docker Repository entity.
    """

    def __init__(self, info: am.DockerRepositoryDetails):
        """
        Constructor for the DockerRepository class.

        Parameters
        ----------
        info :
            The DockerRepositoriesDetails response.
        """
        super().__init__(info.id, info.name)
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
