"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""
from typing import Optional


class BaseError(Exception):
    """
    Base class for creating custom exception classes.

    Attributes:
        message (str): Information about the error that occurred.
    """

    def __init__(
        self,
        message: str,
        detail: Optional[str] = None,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
    ) -> None:
        """
        Initializes the BaseError object.

        Args:
            message (str): Information about the error that occurred.
        """
        super().__init__()

        self.message = message
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code

    def __str__(self):
        """error message for exception"""
        return (
            f"Message: {self.message}, "
            f"Detail: {self.detail}, "
            f"Error Code: {self.error_code}"
        )


class ServerError(BaseError):
    """
    Custom exception class for handling errors that occur in server-related
    operations. This will capture all 5xx errors
    """

    def __init__(
        self,
        message: str,
        detail: Optional[str] = None,
        status_code: Optional[int] = 500,
        error_code: Optional[str] = None,
    ) -> None:
        """
        Initializes the BaseError object.

        Args:
            message (str): Information about the error that occurred.
        """
        super().__init__(
            message=message,
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class UserError(BaseError):
    """
    Custom exception class for user-defined errors. This will capture
    all 4xx errors
    """

    def __init__(
        self,
        message: str,
        detail: Optional[str] = None,
        status_code: Optional[int] = 400,
        error_code: Optional[str] = None,
    ) -> None:
        """
        Initializes the BaseError object.

        Args:
            message (str): Information about the error that occurred.
        """
        super().__init__(
            message=message,
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class ServerNotReachableError(ServerError):
    """Error thrown when the client is unable to connect to the server"""


class ErrorMessages:  # pylint: disable=too-few-public-methods
    """Class that that holds all error messages used in the sdk"""

    SDK_USER_ERR_01_INVALID_AUTH = "Invalid Authentication Config"
    SDK_SERVER_ERR_01_NOT_REACHABLE = "Server not reachable"
