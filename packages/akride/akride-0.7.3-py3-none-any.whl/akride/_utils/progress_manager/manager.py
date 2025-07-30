import threading
from typing import List

from akride import logger
from akride._utils.progress_manager.progress_step import ProgressStep
from akride.core.models.progress_info import ProgressInfo


class ProgressManager:
    def __init__(self):
        self._msg = None
        self._error = None

        self._complete = False
        self._failed = False

        self._steps: List[ProgressStep] = []

        self._register_lock = threading.Lock()

    def set_msg(self, msg):
        self._msg = msg

    def set_error(self, error):
        self._error = error
        self._failed = True

    def set_completed(self):
        self._complete = True

    def is_completed(self):
        return self._complete

    def has_failed(self):
        return self._failed

    def get_error(self):
        return self._error

    def register_step(self, step_name, weight: int = 1) -> ProgressStep:
        with self._register_lock:
            if step_name in self._steps:
                raise ValueError("Step is already registered!")

            step = ProgressStep(step_name=step_name, weight=weight)
            self._steps.append(step)
        return step

    def get_progress_report(self) -> ProgressInfo:
        total_percentage, total_weight = 0, 0

        if not self._steps:
            return ProgressInfo(percent_completed=0.0)

        for step in self._steps:
            weight = step.get_weight()
            progress_report: ProgressInfo = step.get_progress_report()
            total_percentage += weight * progress_report.percent_completed
            total_weight += weight

            logger.debug(
                f"Total percentage {total_percentage}, "
                f"total_weight {total_weight}, "
                f"Step name: {step.get_name()}, "
                f"progress percentage: {progress_report.percent_completed}, "
                f"weight: {step.get_weight()}"
            )

        percentage_completed = float(total_percentage / total_weight)

        return ProgressInfo(
            percent_completed=percentage_completed,
            message=self._msg,
            completed=self._complete,
            error=self._error,
            failed=self._failed,
        )
