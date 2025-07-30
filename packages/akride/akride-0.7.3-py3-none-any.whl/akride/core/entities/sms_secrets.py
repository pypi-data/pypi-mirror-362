"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""

import akridata_akrimanager_v2 as am

from akride.core.entities.entity import Entity


class SMSSecrets(Entity):
    """
    Class representing a SMS Secrets entity.
    """

    def __init__(self, info: am.SMSSecretDetailedResponse):
        """
        Constructor for the SMSSecrets class.

        Parameters
        ----------
        info :
            The SMSSecrets response.
        """
        super().__init__(info.id, info.key)
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
