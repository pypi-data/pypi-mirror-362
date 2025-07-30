import importlib

from akride import logger


class ClassExecutor:
    def __init__(self, module_path: str, klass_name: str):
        self._class_name = klass_name
        self._class_instance = self._get_class_instance(
            module_path=module_path, klass_name=klass_name
        )

    def call_method(self, method_name: str, **kwargs):
        try:
            _method = getattr(self._class_instance, method_name)
            _method(**kwargs)
        except AttributeError:
            raise ValueError(
                f"Method '{method_name}' not found in '{self._class_name}'."
            )

    @classmethod
    def _get_class_instance(cls, module_path: str, klass_name: str):
        _module = cls._get_module(module_path=module_path)

        try:
            # Get the class dynamically
            _MyClass = getattr(_module, klass_name)

            # Create an instance of the class
            return _MyClass()
        except AttributeError:
            raise ValueError(
                f"Class '{klass_name}' not found in module '{module_path}'."
            )

    @staticmethod
    def _get_module(module_path: str):
        try:
            # Import the module dynamically
            return importlib.import_module(module_path)
        except ModuleNotFoundError:
            logger.error(f"Module '{module_path}' not found.")
