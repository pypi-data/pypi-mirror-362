from typing import Optional, Tuple

from akride._utils.resource_utils import get_conf_absolute_path
from akride.core._log import get_logger
from akride.core.constants import Constants

logger_config_file = get_conf_absolute_path(
    file_name=Constants.LOG_CONFIG_FILE_NAME
)

logger = get_logger(module=__name__, config_file_path=logger_config_file)


from importlib_metadata import (  # noqa: E501, E402
    PackageNotFoundError,
    version,
)

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError


from akride.client import AkriDEClient  # noqa F401
from akride.core.entities.jobs import JobSpec  # noqa F401
from akride.core.enums import JobContext, JobStatisticsContext  # noqa F401

# Create a client instance
#


def init(
    sdk_config_tuple: Optional[Tuple[str, str]] = None,
    sdk_config_dict: Optional[dict] = None,
    sdk_config_file: Optional[str] = "",
) -> AkriDEClient:
    """
    Initializes the AkriDEClient with the saas_endpoint and api_key values
    The init params could be passed in different ways, incase multiple
    options are used to pass the init params the order of preference
    would be
    1. sdk_config_tuple, 2. sdk_config 3. sdk_config_file

    Get the config by signing in to Data Explorer UI and navigating to
    Utilities → Get CLI/SDK config
    Parameters
    ----------
    sdk_config_tuple: tuple
        A tuple consisting of saas_endpoint and api_key in that order
    sdk_config_dict: dict
        dictionary containing "saas_endpoint" and "api_key"
    sdk_config_file: str
        Path to the the SDK config file downloaded from Dataexplorer

    Raises
    ---------
        InvalidAuthConfigError: if api-key/host is invalid
        ServerNotReachableError: if the server is unreachable
    """
    return AkriDEClient(
        sdk_config_tuple=sdk_config_tuple,
        sdk_config_dict=sdk_config_dict,
        sdk_config_file=sdk_config_file,
    )
