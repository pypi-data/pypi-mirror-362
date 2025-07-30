from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from akride.core.entities.entity import Entity
from akride.core.types import ClientManager


class Manager(ABC):
    """
    Abstract base class representing a manager for entities.
    """

    def __init__(self, cli_manager: ClientManager):
        """
        Constructor for the Manager class.

        Parameters
        ----------
        client : AkriDEClient
            An instance of the API client.
        """
        self.client_manager = cli_manager

    @abstractmethod
    def create_entity(self, spec: Any) -> Optional[Entity]:
        """
        Creates a new entity.

        Parameters
        ----------
        spec : Dict[str, Any]
            The entity spec.

        Returns
        -------
        Entity
            The created entity
        """

    @abstractmethod
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

    @abstractmethod
    def get_entities(self, attributes: Dict[str, Any]) -> List[Entity]:
        """
        Retrieves information about entities that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any]
            The filter specification. It may have the following optional
            fields

        Returns
        -------
        List[Entity]
            A list of Entity objects.
        """

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
        attrs = {"search_key": name}
        entity_list = self.get_entities(attrs)
        if entity_list is None:
            return None

        for entity in entity_list:
            if entity.name == name:
                return entity
        return None
