"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""
from typing import Optional, Union

import akridata_dsp as dsp

from akride.core.entities.entity import Entity


class Resultset(Entity):
    """
    Class representing a result set entity.
    """

    def __init__(
        self,
        info: Union[
            dsp.ResultsetListResponseItem, dsp.ResultsetGetResponseItem
        ],
        entity_id: Optional[str] = None,
    ):
        """
        Constructor for the Resultset class.

        Parameters
        ----------
        info : dsp.ResultsetListResponseItem
            The resultset response.
        """
        entity_id = entity_id if entity_id else info.id

        super().__init__(entity_id, info.name)
        self.info = info

    @property
    def job_id(self):
        return self.info.request_id

    @property
    def version(self):
        return self.info.version

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
