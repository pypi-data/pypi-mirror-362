"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""
import json
from functools import wraps
from json import JSONDecodeError
from typing import Callable, Union

from akridata_akrimanager_v2 import ApiException as AMException
from akridata_dsp import ApiException as DSException
from urllib3.exceptions import MaxRetryError

from akride.core.exceptions import (
    ErrorMessages,
    ServerError,
    ServerNotReachableError,
    UserError,
)


def translate_api_exceptions(func: Callable) -> Callable:
    """
    Decorator function that catches exceptions raised by the 'DSException'
    and 'AMException' classes and translates them into 'UserError' or
    'ServerError' exceptions.

    Args:
        func: The function to be decorated.

    Returns:
        The decorated function.

    Raises:
        UserError: If the original exception is an instance of
        'DSException'.
        ServerError: If the original exception is an instance of
        'AMException'.
        Exception: If the original exception is not an instance of
        'DSException' or 'AMException'.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as original_exception:
            if isinstance(original_exception, (DSException, AMException)):
                # pylint: disable=W0707
                raise _translate_exception(original_exception) from None
            if isinstance(original_exception, MaxRetryError):
                raise ServerNotReachableError(
                    message=ErrorMessages.SDK_SERVER_ERR_01_NOT_REACHABLE
                )
            if isinstance(original_exception, ValueError):
                raise ServerError(message=str(original_exception))
            raise original_exception

    return wrapper


def _translate_exception(
    ex: Union[AMException, DSException]
) -> Union[UserError, ServerError]:
    """
    Translates exceptions raised by the 'AMException' and 'DSException'
    classes into 'UserError' or 'ServerError' exceptions.

    Args:
        ex: The original exception that was raised.

    Returns:
        UserError or ServerError: Depending on the status code of the original
        exception.
    """

    error_code, message, details = None, None, None

    if ex.body:
        try:
            data = json.loads(ex.body)
            error_code = data.get("code")
            message = data.get("message")
            details = data.get("details")
        except JSONDecodeError:
            message = ex.body

    if ex.status and ex.status >= 500:
        return ServerError(
            message=message,
            detail=details,
            status_code=ex.status,
            error_code=error_code,
        )

    return UserError(
        message=message,
        detail=details,
        status_code=ex.status,
        error_code=error_code,
    )


def _get_error_message(ex: Union[AMException, DSException]) -> str:
    message = ""
    if ex.reason:
        message = f"Reason: {ex.reason}\n"
    if ex.body:
        message += f"Detail: {ex.body}\n"
    return message
