import importlib.util
import inspect
from pathlib import Path
from typing import Iterable, Type

from loguru import logger


def dynamically_import_modules(
    module_paths: Iterable[str],
    is_ignore_error: bool = True,
    target_subclasses: Iterable[Type[object]] = [],
) -> set[Type[object]]:
    """
    Dynamically imports modules from the specified file paths.

    Args:
        module_paths (Iterable[str]): The file paths of the modules to import.
        is_ignore_error (bool, optional): Whether to ignore any errors that occur during the import process. Defaults to True.

    Raises:
        Exception: If an error occurs during the import process and `is_ignore_error` is False.
    """
    all_loaded_classes: list[Type[object]] = []

    for module_path in module_paths:
        file_path = Path(module_path).resolve()
        module_name = file_path.stem
        logger.info(f"[MODULE IMPORT] Import module path: {file_path}")
        # Create a module specification
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            logger.warning(
                f"[DYNAMICALLY MODULE IMPORT] Could not create spec for {module_name}"
            )
            continue

        # Create a new module based on the specification
        module = importlib.util.module_from_spec(spec)
        if spec.loader is None:
            logger.warning(
                f"[DYNAMICALLY MODULE IMPORT] No loader found for {module_name}"
            )
            continue

        # Execute the module in its own namespace

        logger.info(f"[DYNAMICALLY MODULE IMPORT] Import module: {module_name}")
        try:
            spec.loader.exec_module(module)
            logger.success(
                f"[DYNAMICALLY MODULE IMPORT] Successfully imported {module_name}"
            )
        except Exception as error:
            logger.warning(error)
            if not is_ignore_error:
                raise error

        loaded_classes = []
        for attr in dir(module):
            obj = getattr(module, attr)
            if attr.startswith("__"):
                continue
            if not inspect.isclass(obj):
                continue
            loaded_classes.append(obj)
        all_loaded_classes.extend(loaded_classes)

    returned_target_classes: set[Type[object]] = set()
    for target_cls in target_subclasses:
        for loaded_class in all_loaded_classes:
            if loaded_class in target_subclasses:
                continue
            if issubclass(loaded_class, target_cls):
                returned_target_classes.add(loaded_class)

    return returned_target_classes
