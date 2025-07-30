from tqdm import tqdm


class ProgressBarHelper:
    def __init__(self, iterable=None, total=None, **kwargs):
        self._progress_bar = tqdm(iterable=iterable, total=total, **kwargs)

    def __iter__(self):
        return self._progress_bar.__iter__()

    def __enter__(self):
        return self

    def update(self, n=1):
        self._progress_bar.update(n)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._progress_bar.close()
