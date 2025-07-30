import akridata_akrimanager_v2 as am

from akride.core.entities.entity import Entity


class Pipeline(Entity):
    """
    Class representing a Pipeline entity.
    """

    def __init__(self, info: am.Pipeline):
        """
        Constructor for the Pipeline class.
        """
        super().__init__(info.pipeline_id, info.pipeline_name)
        self.info = info

    def delete(self) -> None:
        raise NotImplementedError()
