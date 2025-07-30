"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""

from typing import Any, Dict, List, Optional

import akridata_akrimanager_v2 as am

from akride._utils.exception_utils import translate_api_exceptions
from akride.core._entity_managers.manager import Manager
from akride.core.entities.sms_secrets import SMSSecrets
from akride.core.types import ClientManager


class SMSManager(Manager):
    def __init__(self, cli_manager: ClientManager):
        super().__init__(cli_manager)
        self.sms_api = am.SmsApi(cli_manager.am_client)

    def create_entity(self, spec: Any) -> Optional[SMSSecrets]:
        raise NotImplementedError

    def delete_entity(self, entity: SMSSecrets) -> bool:
        raise NotImplementedError

    @translate_api_exceptions
    def get_entities(self, attributes: Dict[str, Any]) -> List[SMSSecrets]:
        """
        Retrieves information about Secrets that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any], optional
            The filter specification. It has the following fields:
                sms_key : str
                    Filter across SMS keys
                sms_namespace: str
                    Filter across Secret Namespace. Usually the value is 'default'


        Returns
        -------
        List[SMSSecrets]
            A list of Entity objects representing Secrets.
        """
        api_response = self.sms_api.get_sms_secrets(**attributes)
        sms_secrets_list = [SMSSecrets(api_response)]
        return sms_secrets_list
