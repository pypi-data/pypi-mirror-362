"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""

from typing import Dict, Union

import akridata_akrimanager_v2 as am

from akride.core.entities.entity import Entity
from akride.core.enums import DockerImageType


class DockerImage(Entity):
    """
    Class representing a Docker Image entity.
    """

    def __init__(self, info: Union[am.DockerImageItem, am.DockerImageResp]):
        """
        Constructor for the DockerImage class.

        Parameters
        ----------
        info :
            The DockerImageItem response.
        """
        super().__init__(entity_id="", name="")
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


class DockerImageSpec(Dict):
    """
    A Constructor for the DockerImageSpec class.

    Parameters:
    -----------
    name: str
        The display name of the Docker image.
    namespace: str
        The namespace for the Docker image, default is "default".
    description: str
        A brief description of the Docker image.
    repository_id: str
        The repository ID of the Docker repository configured on DE
    image_name: str
        The name of the Docker image.
    image_tag: str
        The tag for the Docker image, default is "latest".
    filter_type: DockerImageType
        The type of filter used by the Docker image,
        default is DockerImageType.FEATURIZER.
    gpu_filter: bool
        A flag indicating if the docker is a GPU filter, default is True.
    allow_no_gpu: bool
        A flag indicating if no GPU is allowed, default is True.
    command: str
        The command to be executed in the Docker image.
    properties: Dict[str, Any]
        Additional properties for DockerImageType.FEATURIZER.
    gpu_mem_fraction: float
        The fraction of GPU memory to be used, must be > 0 if gpu_filter is True.

    Raises
    -------
    ValueError: If `image_name` is empty.
    ValueError: If `command` is empty.
    ValueError: If `gpu_mem_fraction` is <= 0 when `gpu_filter` is True.
    ValueError: If properties are missing for filter type `DockerImageType.FEATURIZER`.
    ValueError: If number of features, patch width, or
    length are empty or non-positive for filter type `DockerImageType.FEATURIZER`.
    """

    def __init__(self, **kwargs):
        defaults = {
            "name": "",
            "namespace": "default",
            "description": "",
            "repository_id": "",
            "image_name": "",
            "image_tag": "latest",
            "filter_type": DockerImageType.FEATURIZER,
            "gpu_filter": True,
            "allow_no_gpu": True,
            "command": "",
        }
        super().__init__()
        self.update(defaults)
        self.update(kwargs)
        if not self["image_name"]:
            raise ValueError("Image name cannot be empty")
        if not self["name"]:
            self["name"] = self["image_name"]
        if self["gpu_filter"]:
            if not self["gpu_mem_fraction"] or self["gpu_mem_fraction"] <= 0.0:
                raise ValueError("GPU memory fraction should be > 0")
        if not self["command"]:
            raise ValueError("Command cannot be empty")
        if (
            self["filter_type"] in [DockerImageType.FEATURIZER]
            and not self["properties"]
        ):
            raise ValueError("Properties missing for Filter Type")
        if self["filter_type"] == DockerImageType.FEATURIZER:
            if not self["properties"]["f"]:
                raise ValueError(
                    "Property: Number of Features cannot be Empty"
                )
            if self["properties"]["m"] <= 0 or self["properties"]["n"] <= 0:
                raise ValueError(
                    "Property: Patch Width or \
                    Length Cannot be 0 or negative should be >=1"
                )
