from platform import system


def is_windows_os() -> bool:
    return _get_os_type() == "Windows"


def is_linux_os() -> bool:
    return _get_os_type() == "Linux"


def is_mac_os() -> bool:
    return _get_os_type() == "Darwin"


def _get_os_type() -> str:
    return system()
