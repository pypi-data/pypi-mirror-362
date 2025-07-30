from __future__ import annotations

import sys
from functools import wraps
from importlib import import_module, metadata
from typing import Callable, Optional

from ._helpers import check_version, split_name_op_version


def require_package(name_op_version: str) -> Callable:
    """
    Decorator to check if required package is installed.

    Parameters
    ----------
    name_op_version : str
        The package name, optionally with an operator and version.

    Raises
    ------
    ModuleNotFoundError
        If the package is not installed or the version does not meet the requirement.

    """
    name, op, required_version = split_name_op_version(name_op_version)

    def decorator(func: Callable):
        """Decorate function."""
        error_message = (
            f"{func.__name__} requires package '{name_op_version.replace(' ', '')}'"
        )

        try:
            import_module(name)

        except ModuleNotFoundError:
            raise ModuleNotFoundError(error_message)

        if required_version:
            current_version = metadata.version(name)
            current_version = tuple(
                map(lambda x: int(x) if x.isdigit() else x, current_version.split("."))
            )

            if not check_version(current_version, required_version, op):
                raise ModuleNotFoundError(error_message)

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Wrap function."""
            return func(*args, **kwargs)

        return wrapper

    return decorator


def require_python(op_version: str) -> Callable:
    """
    Decorator to check if the current Python version meets the required version.

    Parameters
    ----------
    op_version : str
        The required Python version.

    Raises
    ------
    RuntimeError
        If the current Python version does not meet the requirement.

    """
    _, op, required_version = split_name_op_version(op_version)

    def decorator(func: Callable):
        if not check_version(sys.version_info[:3], required_version, op):
            print(sys.version_info)
            raise RuntimeError(
                f"{func.__name__} requires python{op_version.replace(' ', '')}"
            )

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Wrap function."""
            return func(*args, **kwargs)

        return wrapper

    return decorator
