from typing import List, Optional

import akridata_akrimanager_v2 as am
from akridata_akrimanager_v2 import (
    PipelineAttributeGenerator,
    PipelineDocker,
    PostPipelineResp,
)

from akride._utils.exception_utils import translate_api_exceptions
from akride._utils.pipeline.pipeline_helper import PipelineHelper
from akride.core._entity_managers.manager import Manager
from akride.core.entities.docker_pipeline import (
    DockerPipeline,
    DockerPipelineSpec,
)
from akride.core.entities.pipeline import Pipeline
from akride.core.enums import DataType
from akride.core.types import ClientManager


class DockerPipelineManager(Manager):
    def __init__(self, cli_manager: ClientManager):
        super().__init__(cli_manager)
        self.pipeline_api = am.PipelineApi(cli_manager.am_client)

    def _create_pipeline(
        self,
        pipeline_name: str,
        pipeline_description: str,
        pre_processor_docker: PipelineDocker,
        featurizer_docker: PipelineDocker,
        thumbnail_docker: PipelineDocker,
        data_type: Optional[str] = DataType.IMAGE,
        namespace: Optional[str] = "default",
        attribute_generator_dockers: Optional[
            List[PipelineAttributeGenerator]
        ] = None,
    ) -> DockerPipeline:
        docker_pipeline_details_req = (
            PipelineHelper.get_docker_pipeline_detail_request(
                pipeline_name=pipeline_name,
                pipeline_description=pipeline_description,
                pre_processor_docker=pre_processor_docker,
                featurizer_docker=featurizer_docker,
                thumbnail_docker=thumbnail_docker,
                data_type=data_type,
                namespace=namespace,
                attribute_generator_dockers=attribute_generator_dockers,
            )
        )
        response: PostPipelineResp = self.pipeline_api.create_pipeline(
            pipeline_details=docker_pipeline_details_req
        )
        docker_pipeline = DockerPipeline(info=response)
        docker_pipeline.id = response.pipeline_id
        docker_pipeline.name = pipeline_name
        return docker_pipeline

    def create_entity(
        self, spec: DockerPipelineSpec
    ) -> Optional[DockerPipeline]:
        """
        Creates a new Docker Pipeline.

        Parameters
        ----------
        spec : DockerPipeline
            The Docker Pipeline spec.
        Returns
        -------
        Entity
            The created Docker Pipeline
        """
        return self._create_pipeline(**spec)

    def delete_entity(self, entity: DockerPipeline) -> bool:
        raise NotImplementedError

    @translate_api_exceptions
    def get_entities(self, entity: Pipeline) -> Optional[DockerPipeline]:
        raise NotImplementedError
