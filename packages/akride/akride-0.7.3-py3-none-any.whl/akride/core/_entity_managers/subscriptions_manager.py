"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""
from typing import Any, Dict, List, Optional

import akridata_akrimanager_v2 as am
from akridata_akrimanager_v2 import DeSoftwareSpec, DeSoftwareSpecResponse

from akride._utils.exception_utils import translate_api_exceptions
from akride.core._entity_managers.manager import Manager
from akride.core.entities.entity import Entity
from akride.core.types import ClientManager


class SubscriptionsManager(Manager):
    def __init__(self, cli_manager: ClientManager):
        super().__init__(cli_manager)
        self.subscriptions_api = am.SubscriptionsApi(cli_manager.am_client)

    @translate_api_exceptions
    def get_server_version(self):
        response: DeSoftwareSpecResponse = (
            self.subscriptions_api.get_software_spec()
        )  # type: ignore
        assert response.data is not None
        spec: DeSoftwareSpec = response.data
        return spec.version

    def create_entity(self, spec: Any) -> Optional[Entity]:
        raise NotImplementedError

    def delete_entity(self, entity: Entity) -> bool:
        raise NotImplementedError

    def get_entities(self, attributes: Dict[str, Any]) -> List[Entity]:
        raise NotImplementedError
