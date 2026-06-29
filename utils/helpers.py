"""
CandidateOne Helper Utilities

Reusable utility functions shared across the CandidateOne ETL pipeline.

Author: Shankar Irla
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


# ==========================================================
# FILE UTILITIES
# ==========================================================

def ensure_directory(path: str | Path) -> Path:
    """
    Creates a directory if it does not exist.

    Parameters
    ----------
    path : str | Path

    Returns
    -------
    Path
        Path object representing the directory.
    """

    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def file_exists(path: str | Path) -> bool:
    """
    Checks whether a file exists.
    """

    return Path(path).is_file()


def get_extension(path: str | Path) -> str:
    """
    Returns lowercase file extension.

    Example
    -------
    resume.PDF -> .pdf
    """

    return Path(path).suffix.lower()


# ==========================================================
# JSON UTILITIES
# ==========================================================

def load_json(path: str | Path) -> Dict[str, Any]:
    """
    Safely loads a JSON file.

    Raises
    ------
    FileNotFoundError
    json.JSONDecodeError
    """

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(
    data: Dict[str, Any],
    path: str | Path,
    indent: int = 4
) -> None:
    """
    Saves dictionary as JSON.
    """

    path = Path(path)

    ensure_directory(path.parent)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=indent,
            ensure_ascii=False
        )


# ==========================================================
# TEXT UTILITIES
# ==========================================================

def clean_text(text: Optional[str]) -> Optional[str]:
    """
    Normalizes whitespace.

    Example
    -------
    '  John    Doe '

    becomes

    'John Doe'
    """

    if text is None:
        return None

    return " ".join(str(text).strip().split())


def normalize_case(text: Optional[str]) -> Optional[str]:
    """
    Converts text into title case.

    Example
    -------
    Shankar IRLA

    becomes

    shankar irla
    """

    if not text:
        return text

    return clean_text(text).title()


def is_blank(value: Any) -> bool:
    """
    Returns True if value is None or empty.
    """

    if value is None:
        return True

    if isinstance(value, str):
        return value.strip() == ""

    if isinstance(value, (list, dict, tuple, set)):
        return len(value) == 0

    return False


# ==========================================================
# COLLECTION UTILITIES
# ==========================================================

def remove_duplicates(values: Iterable[Any]) -> List[Any]:
    """
    Removes duplicates while preserving order.

    Example
    -------
    [A, B, A, C]

    becomes

    [A, B, C]
    """

    seen = set()
    result = []

    for item in values:

        key = (
            item.lower()
            if isinstance(item, str)
            else item
        )

        if key not in seen:
            seen.add(key)
            result.append(item)

    return result


def flatten(items: Iterable[Iterable[Any]]) -> List[Any]:
    """
    Flattens nested lists.

    Example
    -------
    [[1,2],[3],[4]]

    ->

    [1,2,3,4]
    """

    result = []

    for group in items:
        result.extend(group)

    return result


# ==========================================================
# DICTIONARY UTILITIES
# ==========================================================

def remove_none(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Removes keys whose values are None.
    """

    return {
        key: value
        for key, value in data.items()
        if value is not None
    }


def merge_unique_lists(
    first: List[Any],
    second: List[Any]
) -> List[Any]:
    """
    Merges two lists while preserving order and uniqueness.
    """

    return remove_duplicates(first + second)


# ==========================================================
# NUMERIC UTILITIES
# ==========================================================

def safe_float(value: Any) -> Optional[float]:
    """
    Converts a value to float.

    Returns
    -------
    float | None
    """

    try:
        return float(value)

    except (TypeError, ValueError):
        return None


def clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 1.0
) -> float:
    """
    Restricts a value to a specified range.

    Example
    -------
    clamp(1.3)

    ->

    1.0
    """

    return max(minimum, min(maximum, value))


# ==========================================================
# DEBUGGING
# ==========================================================

def pretty_json(data: Dict[str, Any]) -> str:
    """
    Returns formatted JSON string.

    Useful for debugging and logging.
    """

    return json.dumps(
        data,
        indent=4,
        ensure_ascii=False
    )