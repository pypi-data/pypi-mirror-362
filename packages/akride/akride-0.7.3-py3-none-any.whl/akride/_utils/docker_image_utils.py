from typing import Dict, Optional

from akridata_akrimanager_v2 import DockerImageReq

from akride import Constants
from akride.core.enums import OutputPortType


def _prepare_output_port_properties(properties: Dict[str, int]):
    feature_m = int(properties.get("m", Constants.DEFAULT_FEATURE_VALUE))
    feature_n = int(properties.get("n", Constants.DEFAULT_FEATURE_VALUE))
    output_port = (
        OutputPortType.patch
        if feature_m * feature_n != 1
        else OutputPortType.full
    )
    return {output_port: properties}


def get_featurizer_docker_image_request(
    name: str,
    namespace: str,
    description: str,
    repository_id: str,
    image_name: str,
    image_tag: str,
    filter_type: str,
    command: str,
    properties: Dict[str, int],
    gpu_filter: Optional[bool] = None,
    gpu_mem_fraction: Optional[float] = None,
    allow_no_gpu: bool = True,
) -> DockerImageReq:
    return DockerImageReq(
        name=name,
        namespace=namespace,
        repository_id=repository_id,
        image_name=image_name,
        image_tag=image_tag,
        filter_type=filter_type,
        gpu_filter=gpu_filter,
        gpu_mem_fraction=gpu_mem_fraction,
        allow_no_gpu=allow_no_gpu,
        output_port_properties=_prepare_output_port_properties(properties),
        command=command,
        description=description,
    )
