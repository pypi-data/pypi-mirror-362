from __future__ import annotations

import re
from typing import Literal, Optional


def check_version(
    current_version: tuple[int | str],
    required_version: tuple[int | str],
    op: Optional[Literal["<", "<=", "==", ">=", ">"]] = None,
) -> bool:
    """
    Check if the current version satisfies the required version based on the operator.

    Parameters
    ----------
    current_version : tuple[int | str]
        The current version.
    required_version : tuple[int | str]
        The required version.
    op : {'<', '<=', '==', '>=', '>'}, optional
        The operator to use for comparison.

    Returns
    -------
    bool
        True if the current version satisfies the required version based on the operator,
        False otherwise.

    """
    op = op if op else ">="

    if op == "<":
        return current_version < required_version

    elif op == "<=":
        return current_version <= required_version

    elif op == "==":
        return current_version == required_version

    elif op == ">=":
        return current_version >= required_version

    elif op == ">":
        return current_version > required_version

    else:
        raise ValueError(f"invalid operator '{op}'")


def split_name_op_version(
    name_op_version: str,
) -> tuple[str | None, str | None, tuple[int | str] | None]:
    """
    Split a string of the form "name op version" into its components.

    Parameters
    ----------
    name_op_version : str
        The string to split.

    Returns
    -------
    str | None
        The name of the package.
    str | None
        The operator used for version comparison.
    tuple[int | str] | None
        The version of the package.

    """
    match = re.match(
        r"^\s*(?:(?P<name>\w+)\s*)?(?:(?P<op><=|>=|==|<|>)\s*)?(?P<version>\d+(?:[\.\w-]+)*)?\s*$",
        name_op_version,
    )

    if not match:
        raise ValueError(
            f"could not split '{name_op_version}' into ([name], op, version)"
        )

    name = match.group("name")
    op = match.group("op")
    version = match.group("version")

    if version:
        version = list(map(lambda x: int(x) if x.isdigit() else x, version.split(".")))

        if len(version) < 2:
            version.append(0)

        if len(version) < 3:
            version.append(0)

        version = tuple(version)

    return name, op, version
