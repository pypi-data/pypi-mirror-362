# flake8: noqa  E501
import io
from typing import Any, Dict, List, Optional

import akridata_dsp as dsp
from PIL import Image

from akride import logger
from akride._utils.background_task_helper import BackgroundTask
from akride._utils.exception_utils import translate_api_exceptions
from akride.core._entity_managers.manager import Manager
from akride.core.entities.entity import Entity
from akride.core.entities.jobs import Job
from akride.core.entities.resultsets import Resultset
from akride.core.enums import DatastoreType
from akride.core.types import ClientManager, SampleInfoList

from akridata_dsp import (  # isort:skip
    ApiException,
    ResultsetGetResponse,
    ResultsetListResponse,
)


class ResultsetManager(Manager):
    """Manager resultset operations"""

    def __init__(self, cli_manager: ClientManager):
        super().__init__(cli_manager)
        self.resultset_api = dsp.ResultsetApi(self.client_manager.dsp_client)
        self.image_api = dsp.ImageFetchApi(self.client_manager.dsp_client)

    @translate_api_exceptions
    def create_entity(self, spec: Dict[str, Any]) -> Optional[Resultset]:
        """
        Creates a new resultset.

        Parameters
        ----------
        spec : Dict[str, Any]
            The resultset spec. The spec should have the following fields:
                job: Job
                    The associated job object.
                name : str
                    The name of the new resultset.
                samples: SampleInfoList
                    The samples to be included in this resultset.

        Returns
        -------
        Entity
            The created resultset
        """
        return self._create_resultset(**spec)

    def _create_resultset(
        self, job: Job, name: str, samples: SampleInfoList
    ) -> Optional[Resultset]:
        logger.debug("Creating resultset: %s", name)
        job_id = job.id
        if "dataset_id" in job.info.to_dict():
            dataset_id = job.info.dataset_id  # type: ignore
        else:
            dataset_id = None
        request_id = job_id
        frames = [{"point_id": i} for i in samples.get_point_ids()]
        resultset_request = dsp.ResultsetCreateRequest(
            dataset_id=dataset_id,
            frames=frames,
            name=name,
            tags=None,
        )

        api_response = self.resultset_api.create_resultset(
            request_id=request_id,
            resultset_create_request=resultset_request,
        )
        assert api_response is not None
        return Resultset(api_response)  # type: ignore

    @translate_api_exceptions
    def update_resultset(
        self,
        resultset: Resultset,
        add_list: Optional[SampleInfoList] = None,
        del_list: Optional[SampleInfoList] = None,
    ) -> bool:
        """
        Updates a resultset.

        Parameters
        ----------
        resultset: Resultset
            The resultset to be updated.
        add_list: SampleInfoList, optional
            The list of samples to be added.
        del_list: SampleInfoList, optional
            The list of samples to be deleted.

        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        if add_list is None and del_list is None:
            raise ApiException(
                "Either add_list or del_list must be specified."
            )

        job_id = resultset.job_id
        version = resultset.version

        request_id = job_id
        get_frames = lambda samples: (
            []
            if samples is None
            else [{"point_id": i} for i in samples.get_point_ids()]
        )
        frames = {"add": get_frames(add_list), "del": get_frames(del_list)}
        update_request = dsp.ResultsetUpdateRequest(
            frames=frames, version=version
        )

        self.resultset_api.update_resultset(
            resultset_id=resultset.id,
            request_id=request_id,
            resultset_update_request=update_request,
        )
        return True

    @translate_api_exceptions
    def publish(self, resultset: Resultset) -> bool:
        """
        Publishes a resultset.

        Parameters
        ----------
        resultset: Resultset
            The resultset to be updated.
        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """

        update_request = dsp.ResultsetUpdateRequest(
            export_to_top_level=True, version=resultset.version
        )

        self.resultset_api.update_resultset(
            resultset_id=resultset.id,
            request_id=resultset.job_id,
            resultset_update_request=update_request,
        )
        return True

    @translate_api_exceptions
    def delete_entity(self, entity: Entity) -> bool:
        """
        Deletes an entity.

        Parameters
        ----------
        entity : Entity
            The entity object to delete.

        Returns
        -------
        bool
            Indicates whether this entity was successfully deleted
        """
        logger.debug("Deleting entity %s", entity)
        resultset_id = entity.get_id()
        api_response: Dict[str, str] = self.resultset_api.delete_resultset(
            resultset_id
        )  # type: ignore
        return api_response.get("code") == "RESULTSET_DELETED"

    def upload_resultset(
        self,
        name: str,
        store_type: DatastoreType,
    ) -> BackgroundTask:
        # TODO: Currently we do not register a datastore at DE-level, not sure
        # if we should handle this functionality here, if we do, it needs to be
        # generic one, and cannot just assume access_key,secret_key based store
        # access,
        """
        Uploads a resultset.

        Parameters
        ----------
        name : str
            The name of the resultset.
        store_type : DatastoreType
            The type of the data store to upload the resultset to.

        Returns
        -------
        BackgroundTask
            a task object.
        """
        logger.debug("Uploading resultset to %s, %s", name, store_type)
        raise NotImplementedError
        # task = BackgroundTask()
        # return task

    @translate_api_exceptions
    def get_entities(self, attributes: Dict[str, Any]) -> List[Resultset]:
        """
        Retrieves information about entities that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any]
            The filter specification. It may have the following optional
            fields:
                data_type : str
                    The data type to filter on.
                search_key : str
                    Filter across fields like dataset id, and dataset name.

        Returns
        -------
        List[Entity]
            A list of Entity objects representing resultsets.
        """
        attributes = attributes.copy()
        if "search_key" in attributes:
            attributes["search_str"] = attributes["search_key"]
            del attributes["search_key"]
        if "page_number" not in attributes:
            attributes["page_number"] = 1
        if "page_size" not in attributes:
            # TODO: denote a number to mean "unlimited"
            attributes["page_size"] = 1000

        api_response: ResultsetListResponse = (
            self.resultset_api.list_resultsets(**attributes)
        )  # type: ignore
        assert api_response.resultsets is not None
        resultset_list = [Resultset(info) for info in api_response.resultsets]
        return resultset_list

    @translate_api_exceptions
    def get_resultset_by_id(self, resultset_id: str) -> Resultset:
        """
        Retrieves information about entities that have the given attributes.

        Parameters
        ----------
        resultset_id: str

        Returns
        -------
        Resultset
            An Object representing a resultset
        """

        api_response: dsp.ResultsetGetResponse = (
            self.resultset_api.get_resultset(
                resultset_id=resultset_id, page_number=1, page_size=1
            )
        )

        return Resultset(info=api_response.resultset, entity_id=resultset_id)

    @translate_api_exceptions
    def get_samples(
        self, resultset: Resultset, max_sample_size: int = 10000
    ) -> SampleInfoList:
        """
        Retrieves the samples of a resultset

        Parameters
        ----------
        resultset : Resultset
            The Resultset object to get samples for.

        Returns
        -------
        SampleInfoList
            A SampleInfoList object.
        """
        # TODO: denote a number to mean "unlimited" page size
        attributes = {"page_number": 1, "page_size": max_sample_size}
        api_response: ResultsetGetResponse = self.resultset_api.get_resultset(
            resultset.get_id(), **attributes
        )  # type: ignore
        samples = SampleInfoList()
        assert api_response.resultset is not None
        for sample in api_response.resultset.data[0].frames:
            samples.append_sample(sample)
        return samples

    @translate_api_exceptions
    def get_thumbnail_images(
        self, resultset_samples: SampleInfoList
    ) -> List[Image.Image]:
        """
        Retrieves the thumbnails of a resultset

        Parameters
        ----------
        resultset : SampleInfoList
            The SampleInfoList object to get thumbnail URLs from.

        Returns
        -------
        List[Image.Image]
            A list of thumbnail images.
        """
        urls = resultset_samples.get_thumbnail_urls()
        result = []
        # TODO use the async API instead
        for image_path in urls:
            image_path = image_path.replace("/ds/images/", "")
            image_response = self.image_api.fetch_image(
                image_path, _preload_content=False
            )
            result.append(Image.open(io.BytesIO(image_response.data)))  # type: ignore
        return result
