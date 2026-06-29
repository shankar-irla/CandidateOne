"""
Conflict Resolver

Determines which candidate value should be retained when
multiple sources provide conflicting information.

Responsibilities
----------------
Deterministic conflict resolution
Source priority handling
Merge list fields
Merge nested dictionaries
Remove duplicates
Never invent values

"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List


class ConflictResolver:
    """
    Resolves conflicts between candidate records.
    """

    SOURCE_PRIORITY = {
        "resume": 5,
        "linkedin": 4,
        "ats": 3,
        "github": 2,
        "recruiter_csv": 1
    }

    # -----------------------------------------------------
    # Source Priority
    # -----------------------------------------------------

    @classmethod
    def get_priority(
        cls,
        source: str
    ) -> int:
        """
        Returns priority of a source.
        """

        return cls.SOURCE_PRIORITY.get(
            source,
            0
        )

    # -----------------------------------------------------
    # Empty Check
    # -----------------------------------------------------

    @staticmethod
    def is_empty(value: Any) -> bool:
        """
        Determines whether a value should be treated as empty.
        """

        if value is None:
            return True

        if isinstance(value, str):
            return value.strip() == ""

        if isinstance(value, (list, dict)):
            return len(value) == 0

        return False

    # -----------------------------------------------------
    # Primitive Values
    # -----------------------------------------------------

    @classmethod
    def resolve_value(
        cls,
        current_value: Any,
        new_value: Any,
        current_source: str,
        new_source: str
    ) -> Any:
        """
        Resolves conflicting primitive values.
        """

        if cls.is_empty(current_value):
            return new_value

        if cls.is_empty(new_value):
            return current_value

        if cls.get_priority(new_source) >= cls.get_priority(current_source):
            return new_value

        return current_value

    # -----------------------------------------------------
    # Lists
    # -----------------------------------------------------

    @staticmethod
    def merge_lists(
        current: List[Any],
        incoming: List[Any]
    ) -> List[Any]:
        """
        Merges two lists while removing duplicates.
        """

        merged = []

        seen = set()

        for item in current + incoming:

            key = str(item).lower()

            if key in seen:
                continue

            seen.add(key)

            merged.append(item)

        return merged

    # -----------------------------------------------------
    # Dictionaries
    # -----------------------------------------------------

    @classmethod
    def merge_dicts(
        cls,
        current: Dict,
        incoming: Dict,
        current_source: str,
        new_source: str
    ) -> Dict:
        """
        Recursively merges nested dictionaries.
        """

        result = deepcopy(current)

        for key, value in incoming.items():

            if key not in result:

                result[key] = value
                continue

            current_value = result[key]

            if isinstance(current_value, dict) and isinstance(value, dict):

                result[key] = cls.merge_dicts(
                    current_value,
                    value,
                    current_source,
                    new_source
                )

            elif isinstance(current_value, list) and isinstance(value, list):

                result[key] = cls.merge_lists(
                    current_value,
                    value
                )

            else:

                result[key] = cls.resolve_value(
                    current_value,
                    value,
                    current_source,
                    new_source
                )

        return result

    # -----------------------------------------------------
    # Merge Candidate
    # -----------------------------------------------------

    @classmethod
    def merge_candidate(
        cls,
        current: Dict,
        incoming: Dict,
        current_source: str,
        new_source: str
    ) -> Dict:
        """
        Merges two canonical candidate profiles.
        """

        merged = deepcopy(current)

        for field, value in incoming.items():

            if field not in merged:

                merged[field] = deepcopy(value)
                continue

            current_value = merged[field]

            if isinstance(current_value, dict) and isinstance(value, dict):

                merged[field] = cls.merge_dicts(
                    current_value,
                    value,
                    current_source,
                    new_source
                )

            elif isinstance(current_value, list) and isinstance(value, list):

                merged[field] = cls.merge_lists(
                    current_value,
                    value
                )

            else:

                merged[field] = cls.resolve_value(
                    current_value,
                    value,
                    current_source,
                    new_source
                )

        return merged