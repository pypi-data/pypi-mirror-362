from abc import ABC, abstractmethod
from typing import Optional

import akridata_akrimanager_v2 as am

from akride.core._filters.enums import FilterTypes
from akride.core.constants import Constants


class PartitionerFilter(ABC):
    PARTITION_TIME_FRAME = Constants.PARTITION_TIME_FRAME

    def __init__(
        self,
        dataset_id: str,
        ccs_api: am.CcsApi,
        token_size: int,
        partition_size: Optional[int] = None,
    ):
        self._dataset_id = dataset_id
        self._ccs_api = ccs_api

        self._filter_type = FilterTypes.Partitioner

        self._partition_size = partition_size
        self._token_size = token_size

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def cleanup_token(self, token_num: int):
        pass

    @abstractmethod
    def cleanup(self):
        pass
