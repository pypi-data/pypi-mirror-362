import pprint
from abc import ABC, abstractmethod
from typing import Optional


class Entity(ABC):
    """
    Abstract base class representing an entity in the system.
    """

    def __init__(self, entity_id, name: Optional[str] = None) -> None:
        self.id = entity_id  # pylint: disable=invalid-name
        self.name = name

    def get_id(self) -> Optional[str]:
        """
        Method for getting the ID of the entity.

        Returns
        -------
        str
            The ID of the entity.
        """
        if hasattr(self, "id"):
            return self.id

        return None

    def get_name(self) -> Optional[str]:
        """
        Method for getting the name of the entity.

        Returns
        -------
        str
            The name of the entity.
        """
        if hasattr(self, "name"):
            return self.name

        return None

    def to_dict(self) -> dict:
        """
        Method for converting the entity to a dictionary.

        Returns
        -------
        dict
            A dictionary representing the entity.
        """
        return vars(self)

    @abstractmethod
    def delete(self) -> None:
        """
        Deletes an entity.

        Parameters
        ----------

        Returns
        -------
        None
        """

    def __repr__(self) -> str:
        """
        Method for representing this object as a string.

        Returns
        -------
        str
            A formatted string representing the object.
        """
        return pprint.pformat(self.to_dict())
