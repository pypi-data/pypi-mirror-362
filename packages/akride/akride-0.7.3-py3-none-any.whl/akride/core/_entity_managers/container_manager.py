from typing import Any, Dict, List, Optional

import akridata_akrimanager_v2 as am
from akridata_akrimanager_v2 import ListContainerResp

from akride._utils.exception_utils import translate_api_exceptions
from akride.core._entity_managers.manager import Manager
from akride.core.entities.containers import Container
from akride.core.entities.entity import Entity
from akride.core.types import ClientManager


class ContainerManager(Manager):
    """
    Class Managing Container related operations on DataExplorer
    """

    def __init__(self, cli_manager: ClientManager):
        super().__init__(cli_manager)

        self.container_api = am.ContainerApi(cli_manager.am_client)

    def create_entity(self, spec: Any) -> Optional[Entity]:
        raise NotImplementedError

    def delete_entity(self, entity: Entity) -> bool:
        raise NotImplementedError

    @translate_api_exceptions
    def get_entities(
        self, attributes: Optional[Dict[str, Any]] = None
    ) -> List[Entity]:
        """
        Retrieves information about containers that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any], optional
            The filter specification. It may have the following
            optional fields:
                filter_by_name: str
                    Filter by container name.
                search_by_name : str
                    Search by container name.

        Returns
        -------
        List[Entity]
            A list of Entity objects representing containers.
        """
        attributes = attributes if attributes else {}

        attributes["internal"] = False
        api_response: ListContainerResp = self.container_api.list_containers(
            **attributes
        )
        return [Container(info) for info in api_response.containers]
