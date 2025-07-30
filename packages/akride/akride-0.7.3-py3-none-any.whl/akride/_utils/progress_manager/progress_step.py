import threading

from akride.core.models.progress_info import ProgressInfo


class ProgressStep:
    def __init__(self, step_name, weight: int = 1):
        self._step_name = step_name

        self._weight = weight

        self._total_steps = 0
        self._started: bool = False

        self._completed_steps = 0

        self._update_lock = threading.Lock()

    def get_weight(self):
        return self._weight

    def has_started(self):
        return self._started

    def set_total_steps(self, total):
        if not self._started:
            with self._update_lock:
                self._total_steps = total
                self._started = True

    def increment_processed_steps(self, completed):
        if not self._started:
            raise ValueError(
                "Cannot increment processed steps when not started!"
            )

        with self._update_lock:
            self._completed_steps += completed

            if self._completed_steps > self._total_steps:
                self._completed_steps = self._total_steps

    def get_name(self):
        return self._step_name

    def get_progress_report(self) -> ProgressInfo:
        # If not started, mark percentage as 0,
        # Else, if total steps is 0, mark percentage as 100
        #       else, compute the percentage of steps completed
        if not self._started:
            percentage_completed = 0.0
        else:
            if self._total_steps <= 0:
                percentage_completed = 100.0
            else:
                percentage_completed = (
                    float(self._completed_steps / self._total_steps) * 100
                )

        return ProgressInfo(
            percent_completed=percentage_completed,
        )
