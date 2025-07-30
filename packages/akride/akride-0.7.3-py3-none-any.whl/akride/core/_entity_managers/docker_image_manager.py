"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""

from typing import Any, Dict, List, Optional

import akridata_akrimanager_v2 as am
from akridata_akrimanager_v2 import DockerImageResp

from akride import logger
from akride._utils.docker_image_utils import (
    get_featurizer_docker_image_request,
)
from akride._utils.exception_utils import translate_api_exceptions
from akride.core._entity_managers.manager import Manager
from akride.core.entities.docker_image import DockerImage, DockerImageSpec
from akride.core.entities.entity import Entity
from akride.core.enums import DockerImageType
from akride.core.types import ClientManager


class DockerImageManager(Manager):
    def __init__(self, cli_manager: ClientManager):
        super().__init__(cli_manager)
        self.image_api = am.ImageApi(cli_manager.am_client)

    def _create_featurizer_docker_image(
        self,
        name: str,
        namespace: str,
        repository_id: str,
        description: str,
        image_name: str,
        image_tag: str,
        command: str,
        filter_type: Optional[str] = DockerImageType.FEATURIZER,
        gpu_filter: Optional[bool] = None,
        allow_no_gpu: Optional[bool] = None,
        gpu_mem_fraction: Optional[float] = None,
        properties: Optional[Dict[str, int]] = None,
    ) -> Optional[DockerImage]:
        logger.debug(f"Registering docker image : {name}")
        docker_img_req = get_featurizer_docker_image_request(
            name=name,
            namespace=namespace,
            repository_id=repository_id,
            description=description,
            image_name=image_name,
            image_tag=image_tag,
            filter_type=filter_type,
            gpu_filter=gpu_filter,
            allow_no_gpu=allow_no_gpu,
            gpu_mem_fraction=gpu_mem_fraction,
            properties=properties,
            command=command,
        )
        response: DockerImageResp = self.image_api.register_docker_image(
            docker_image_req=docker_img_req
        )
        img = DockerImage(info=response)
        img.id = response.id
        img.name = name
        return img

    def create_entity(self, spec: DockerImageSpec) -> Optional[DockerImage]:
        """
        Creates a new Docker Image.

        Parameters
        ----------
        spec : DockerImageSpec
            The Docker Image spec.
        Returns
        -------
        Entity
            The created Docker Image
        """
        if spec.get("filter_type") == DockerImageType.FEATURIZER:
            return self._create_featurizer_docker_image(**spec)
        else:
            raise NotImplementedError

    def delete_entity(self, entity: DockerImage) -> bool:
        raise NotImplementedError

    def get_entity_by_name(self, name: str) -> Optional[Entity]:
        """
        Retrieves an entity with the given name.

        Parameters
        ----------
        name : str
            The name of the entity to retrieve.

        Returns
        -------
        Entity
            The Entity object.
        """
        attrs = {"filter_by_name": name}
        entity_list = self.get_entities(attrs)
        if entity_list is None:
            return None

        for entity in entity_list:
            if entity.name == name:
                return entity
        return None

    @translate_api_exceptions
    def get_entities(self, attributes: Dict[str, Any]) -> List[DockerImage]:
        """
        Retrieves information about Docker Images that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any], optional
            The filter specification. It may have the following
            optional fields:
                filter_by_name : str
                    Filter across fields like docker name.

        Returns
        -------
        List[Entity]
            A list of Entity objects representing Docker Image.
        """
        api_response = self.image_api.list_docker_image(**attributes)
        docker_image_list = []
        for info in api_response.docker_images:
            docker_img = DockerImage(info)
            docker_img.id = info.id
            docker_img.name = info.name
            docker_image_list.append(docker_img)
        return docker_image_list
