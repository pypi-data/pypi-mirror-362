import importlib.resources

from akride._utils import video_splitter
from akride.core import conf


def _get_absolute_path(module, file_name):
    with importlib.resources.path(module, file_name) as p:
        return str(p)


def get_conf_absolute_path(file_name):
    return _get_absolute_path(conf, file_name)


def get_video_splitter_script(file_name):
    return _get_absolute_path(video_splitter, file_name)
