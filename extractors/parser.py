"""
CandidateOne Generic Parser

Shared parsing utilities used by all extractors.

Responsibilities
----------------
- Safe dictionary access
- String extraction
- List normalization
- URL extraction
- Email extraction
- Phone extraction
- Experience calculation helpers

This module intentionally contains NO source-specific logic.

"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional


class Parser:
    """
    Generic parser helper used by all extractors.
    """

    # -----------------------------------------------------
    # Dictionary Helpers
    # -----------------------------------------------------

    @staticmethod
    def get(
        data: Dict[str, Any],
        key: str,
        default: Any = None
    ) -> Any:
        """
        Safely retrieves a value from a dictionary.
        """

        if not isinstance(data, dict):
            return default

        return data.get(key, default)

    @staticmethod
    def nested_get(
        data: Dict[str, Any],
        *keys,
        default=None
    ):
        """
        Safely retrieves nested dictionary values.

        Example
        -------
        nested_get(data, "profile", "email")
        """

        current = data

        for key in keys:

            if not isinstance(current, dict):
                return default

            current = current.get(key)

            if current is None:
                return default

        return current

    # -----------------------------------------------------
    # Text
    # -----------------------------------------------------

    @staticmethod
    def text(value: Any) -> Optional[str]:
        """
        Cleans text values.
        """

        if value is None:
            return None

        value = str(value)

        value = " ".join(value.split())

        return value if value else None

    # -----------------------------------------------------
    # Lists
    # -----------------------------------------------------

    @staticmethod
    def list(value: Any) -> List[Any]:
        """
        Converts any value into a list.

        None
            -> []

        "Python"
            -> ["Python"]

        ["A","B"]
            -> ["A","B"]
        """

        if value is None:
            return []

        if isinstance(value, list):
            return value

        return [value]

    # -----------------------------------------------------
    # Email
    # -----------------------------------------------------

    EMAIL_PATTERN = re.compile(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    )

    @classmethod
    def emails(cls, text: str) -> List[str]:
        """
        Extracts email addresses.
        """

        if not text:
            return []

        return sorted(set(cls.EMAIL_PATTERN.findall(text)))

    # -----------------------------------------------------
    # Phone
    # -----------------------------------------------------

    PHONE_PATTERN = re.compile(
        r"(?:\+?\d[\d\s().-]{8,}\d)"
    )

    @classmethod
    def phones(cls, text: str) -> List[str]:
        """
        Extracts phone numbers.
        """

        if not text:
            return []

        return sorted(set(cls.PHONE_PATTERN.findall(text)))

    # -----------------------------------------------------
    # URLs
    # -----------------------------------------------------

    URL_PATTERN = re.compile(
        r"https?://[^\s]+"
    )

    @classmethod
    def urls(cls, text: str) -> List[str]:
        """
        Extracts URLs.
        """

        if not text:
            return []

        return sorted(set(cls.URL_PATTERN.findall(text)))

    # -----------------------------------------------------
    # Skills
    # -----------------------------------------------------

    @staticmethod
    def split_skills(value: Any) -> List[str]:
        """
        Converts skills into a list.

        Accepts:

        Python,SQL

        Python | SQL

        Python;SQL

        ["Python","SQL"]
        """

        if value is None:
            return []

        if isinstance(value, list):

            return [
                str(skill).strip()
                for skill in value
                if str(skill).strip()
            ]

        text = str(value)

        separators = ["|", ";", ","]

        for separator in separators:
            text = text.replace(separator, ",")

        return [
            skill.strip()
            for skill in text.split(",")
            if skill.strip()
        ]

    # -----------------------------------------------------
    # Years Experience
    # -----------------------------------------------------

    @staticmethod
    def years(value: Any) -> Optional[float]:
        """
        Converts experience to float.

        Examples
        --------
        "5"

        "5 years"

        5

        5.5
        """

        if value is None:
            return None

        if isinstance(value, (int, float)):
            return float(value)

        match = re.search(
            r"\d+(\.\d+)?",
            str(value)
        )

        if match:
            return float(match.group())

        return None

    # -----------------------------------------------------
    # Boolean
    # -----------------------------------------------------

    @staticmethod
    def boolean(value: Any) -> bool:
        """
        Converts common truthy values.

        yes
        true
        1

        -> True
        """

        if isinstance(value, bool):
            return value

        if value is None:
            return False

        return str(value).strip().lower() in {
            "true",
            "yes",
            "1",
            "y"
        }