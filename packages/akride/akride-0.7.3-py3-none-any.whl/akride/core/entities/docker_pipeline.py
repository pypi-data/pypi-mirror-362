"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""

from typing import Dict, List

import akridata_akrimanager_v2 as am
from akridata_akrimanager_v2 import PipelineAttributeGenerator, PipelineDocker

from akride.core.entities.entity import Entity
from akride.core.enums import DataType


class DockerPipeline(Entity):
    """
    Class representing a Docker Pipeline Entity.
    """

    def __init__(self, info: am.PostPipelineResp):
        """
        Constructor for the DockerPipeline class.

        Parameters
        ----------
        info :
            The PipelineDetails response.
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


class DockerPipelineSpec(Dict):
    """
     A Constructor for the DockerPipelineSpec class.

    Parameters
     ----------
     pipeline_name: str
          The name of the Docker pipeline.
     pipeline_description: str
         A brief description of the Docker pipeline.
     data_type: str
         The type of data processed by the pipeline, default is DataType.IMAGE.value.
     namespace: str
         The namespace for the Docker pipeline, default is "default".
     pre_processor_docker: PipelineDocker
        The Docker image specification for the pre-processor.
     featurizer_docker: PipelineDocker
        The Docker image specification for the featurizer.
     thumbnail_docker: PipelineDocker
        The Docker image specification for the thumbnail generator.
     attribute_generator_dockers :
        List[PipelineAttributeGenerator], optional
        A list of Docker image specifications for attribute generators.


     Raises
     -------
     ValueError: If `pipeline_name` is empty.
     ValueError: If `pipeline_description` is empty.
     ValueError: If `data_type` is not one of the allowed values
        (DataType.IMAGE.value or DataType.VIDEO.value).

    """

    def __init__(
        self,
        pre_processor_docker: PipelineDocker,
        featurizer_docker: PipelineDocker,
        thumbnail_docker: PipelineDocker,
        attribute_generator_dockers: List[PipelineAttributeGenerator] = None,
        **kwargs,
    ):
        defaults = {
            "pipeline_name": "",
            "pipeline_description": "",
            "data_type": DataType.IMAGE.value,
            "namespace": "default",
            "pre_processor_docker": pre_processor_docker,
            "featurizer_docker": featurizer_docker,
            "thumbnail_docker": thumbnail_docker,
            "attribute_generator_dockers": attribute_generator_dockers,
        }
        super().__init__(defaults, **kwargs)
        self.update(defaults)
        self.update(kwargs)
        if not self["pipeline_name"]:
            raise ValueError("Pipeline name is required")
        if not self["pipeline_description"]:
            raise ValueError("Pipeline description is required")
        if self["data_type"] not in [
            DataType.IMAGE.value,
            DataType.VIDEO.value,
        ]:
            raise ValueError(
                f"Choose Data Type from the following: {[el.value for el in DataType]}"
            )
