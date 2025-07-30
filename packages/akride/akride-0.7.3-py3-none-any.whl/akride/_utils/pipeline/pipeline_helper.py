from typing import List, Optional

from akridata_akrimanager_v2 import (
    PipelineAttributeGenerator,
    PipelineDetails,
    PipelineDocker,
)

from akride.core.enums import DataType


class PipelineHelper:
    @staticmethod
    def get_docker_pipeline_detail_request(
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
    ) -> PipelineDetails:
        return PipelineDetails(
            pipeline_name=pipeline_name,
            pipeline_description=pipeline_description,
            pre_processor_docker=pre_processor_docker,
            featurizer_docker=featurizer_docker,
            thumbnail_docker=thumbnail_docker,
            data_type=data_type,
            namespace=namespace,
            attribute_generator_dockers=attribute_generator_dockers,
        )
