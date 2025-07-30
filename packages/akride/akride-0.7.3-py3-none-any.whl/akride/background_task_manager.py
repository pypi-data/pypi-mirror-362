import threading
from typing import Dict

from akride._utils.background_task_helper import BackgroundTask
from akride._utils.progress_manager.manager import ProgressManager
from akride.core.enums import BackgroundTaskType
from akride.core.exceptions import UserError


class BackgroundTaskManager:
    """Helper class to manage background task"""

    def __init__(self):
        self._tasks: Dict[str, BackgroundTask] = {}
        self._lock = threading.Lock()

    def start_task(
        self,
        entity_id: str,
        task_type: BackgroundTaskType,
        target_function,
        *args,
        **kwargs,
    ) -> BackgroundTask:
        """
        Start a background task.

        Parameters
        ----------
        :param task_type: The type of the background task.
        :param entity_id: Entity ID associated with the task
        :param target_function: The target function to run
        :param args: Arguments for the target function
        :param kwargs: Keyword arguments for the target function
        Returns
        -------
        BackgroundTask
           background task object
        """
        with self._lock:
            if self.is_task_running(task_type=task_type, entity_id=entity_id):
                raise UserError(
                    f"Task {task_type.value} for entity {entity_id} already "
                    f"in progress!",
                    status_code=409,
                )

            task_id = self._get_task_id(
                entity_id=entity_id, task_type=task_type
            )

            progress_manager = ProgressManager()
            task = BackgroundTask(
                target_function, progress_manager, *args, **kwargs
            )
            task.start()

            self._tasks[task_id] = task
            return task

    def is_task_running(
        self, entity_id: str, task_type: BackgroundTaskType
    ) -> bool:
        """
        Parameters
        ----------
        :param entity_id: Entity ID associated with the task.
        :param task_type: The type of the background task.
        Returns
        -------
        Boolean
           a boolean representing whether task is running or not.
        """
        task_id = self._get_task_id(entity_id=entity_id, task_type=task_type)
        task = self._tasks.get(task_id)
        if task:
            return not task.has_completed()
        return False

    @staticmethod
    def _get_task_id(entity_id: str, task_type: BackgroundTaskType):
        return f"{task_type.value}_{entity_id}"
