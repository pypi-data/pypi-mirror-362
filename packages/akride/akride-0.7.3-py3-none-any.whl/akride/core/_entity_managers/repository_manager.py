"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""

from typing import Any, Dict, List, Optional

import akridata_akrimanager_v2 as am

from akride._utils.exception_utils import translate_api_exceptions
from akride.core._entity_managers.manager import Manager
from akride.core.entities.docker_repository import DockerRepository
from akride.core.types import ClientManager


class RepositoryManager(Manager):
    def __init__(self, cli_manager: ClientManager):
        super().__init__(cli_manager)
        self.repository_api = am.RepositoryApi(cli_manager.am_client)

    def create_entity(self, spec: Any) -> Optional[DockerRepository]:
        raise NotImplementedError

    def delete_entity(self, entity: DockerRepository) -> bool:
        raise NotImplementedError

    @translate_api_exceptions
    def get_entities(
        self, attributes: Dict[str, Any]
    ) -> List[DockerRepository]:
        """
        Retrieves information about Docker Repositories that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any], optional
            The filter specification. It may have the following
            optional fields:
                search_key : str
                    Filter across fields like repository id, and repository name.

        Returns
        -------
        List[Entity]
            A list of Entity objects representing Repositories.
        """
        attributes = attributes.copy()
        if "search_key" in attributes:
            attributes["search_str"] = attributes["search_key"]
            del attributes["search_key"]
        api_response = self.repository_api.list_repository(**attributes)
        repository_list = [
            DockerRepository(info) for info in api_response.repositories
        ]
        return repository_list
