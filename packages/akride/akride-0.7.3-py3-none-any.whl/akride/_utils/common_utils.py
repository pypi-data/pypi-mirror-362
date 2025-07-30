from typing import Any, List
from uuid import uuid4


def get_random_uuid():
    return uuid4().hex


def get_values_in_batches(values: List[Any], batch_size: int):
    for i in range(0, len(values), batch_size):
        yield values[i : i + batch_size]
