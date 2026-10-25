"""Stateless helpers shared by several agent-kit classes."""

import re
import time
from collections.abc import Callable, Iterable

type JsonValue = (
    str | int | float | bool | None | list["JsonValue"] | dict[str, "JsonValue"]
)

ENV_REF_PATTERN = re.compile(r"\$\{env:([A-Za-z_][A-Za-z0-9_]*)\}")
LOCK_RETRY_ATTEMPTS = 5
LOCK_RETRY_DELAY_SECONDS = 0.2


def unique[T](items: Iterable[T]) -> list[T]:
    """Drop empty and repeated items while keeping the first-seen order.

    :param items: Items in priority order.
    :return: The distinct, non-empty items.
    """
    return list(dict.fromkeys(item for item in items if item))


def split_csv(values: Iterable[str]) -> list[str]:
    """Split comma-separated option values into trimmed, non-empty items.

    :param values: Raw option values such as ``["a,b", "c"]``.
    :return: The individual items, for example ``["a", "b", "c"]``.
    """
    return [
        item.strip() for value in values for item in value.split(",") if item.strip()
    ]


def rewrite_env_refs(value: JsonValue, replacement: str) -> JsonValue:
    """Rewrite every ``${env:NAME}`` inside strings, lists, and dicts.

    :param value: A string, list, dict, or any other value (returned unchanged).
    :param replacement: Regex replacement where ``\\1`` stands for the variable name.
    :return: A copy of ``value`` with the references rewritten.
    """
    if isinstance(value, str):
        return ENV_REF_PATTERN.sub(replacement, value)
    if isinstance(value, list):
        return [rewrite_env_refs(item, replacement) for item in value]
    if isinstance(value, dict):
        return {key: rewrite_env_refs(item, replacement) for key, item in value.items()}
    return value


def retry_on_permission_error(action: Callable[[], object]) -> None:
    """Run a filesystem action, retrying while Windows briefly locks a new file.

    :param action: The action to run, for example a copy or an unlink.
    :raises PermissionError: If the path is still locked after every attempt.
    """
    for attempt in range(LOCK_RETRY_ATTEMPTS):
        try:
            action()
            return
        except PermissionError:
            if attempt == LOCK_RETRY_ATTEMPTS - 1:
                raise
            time.sleep(LOCK_RETRY_DELAY_SECONDS * (attempt + 1))
