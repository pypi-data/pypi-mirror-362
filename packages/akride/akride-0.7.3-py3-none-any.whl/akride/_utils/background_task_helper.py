"""
 Copyright (C) 2024, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""

import threading
import traceback
from typing import Optional

from akride._utils.progress_manager.manager import ProgressManager
from akride.core.models.progress_info import ProgressInfo


class BackgroundTask:
    """
    Class representing asynchronous tasks.
    """

    def __init__(
        self,
        target_function,
        progress_manager: ProgressManager,
        *args,
        **kwargs
    ):
        """
        Constructor for the BackgroundTask class.
        :param target_function: The target function to run
        :param args: Arguments for the target function
        :param kwargs: Keyword arguments for the target function
        """

        self.target_function = target_function
        self.args = args
        self.kwargs = kwargs

        self._result = None

        self._thread = None

        self._progress_manager = progress_manager

    def run_task(self):
        """
        Run the target function and handle any exceptions.
        """
        try:
            self._result = self.target_function(
                self._progress_manager, *self.args, **self.kwargs
            )
        except Exception:
            self._progress_manager.set_error(error=traceback.format_exc())

        self._progress_manager.set_completed()

    def start(self):
        """
        Start the background task in a separate thread.
        """
        self._thread = threading.Thread(target=self.run_task)
        self._thread.start()

    def has_completed(self):
        return self._progress_manager.is_completed()

    def has_failed(self):
        return self._progress_manager.has_failed()

    def get_result(self):
        """
        Get the result of the background task.
        :return: The result of the task
        """

        if self.has_completed():
            return self._result

        raise ValueError("Task is in progress. Please check after some time!")

    def get_error(self) -> Optional[Exception]:
        """
        Get the error if the task encountered an exception.
        :return: The error object
        """
        error = self._progress_manager.get_error()
        if self.has_completed() and error:
            return error

    def get_progress_info(self) -> ProgressInfo:
        """

        Parameters
        ----------

        Returns
        -------
        ProgressInfo
            The progress information
        """
        return self._progress_manager.get_progress_report()

    def wait_for_completion(self) -> ProgressInfo:
        """
        Waits for this task to complete and return the progress information

        Parameters
        ----------

        Returns
        -------
        ProgressInfo
            The progress information
        """
        self._thread.join()
        return self._progress_manager.get_progress_report()
