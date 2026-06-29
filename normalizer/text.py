"""
Text Normalizer

Provides reusable text normalization functions used across
the CandidateOne pipeline.

Responsibilities
----------------
Trim whitespace
Normalize spacing
Normalize names
Normalize titles
Remove special characters
Safe string conversion

"""

from __future__ import annotations

import re
from typing import Optional


class TextNormalizer:
    """
    Generic text normalization utility.
    """

    # -----------------------------------------------------
    # Basic Cleanup
    # -----------------------------------------------------

    @staticmethod
    def clean(text: Optional[str]) -> Optional[str]:
        """
        Removes extra whitespace and newlines.

        Example:
            "  Shankar   Irla  "
                ↓
            "Shankar Irla"
        """

        if text is None:
            return None

        text = str(text)

        text = text.replace("\n", " ")
        text = text.replace("\t", " ")

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # -----------------------------------------------------
    # Name Normalization
    # -----------------------------------------------------

    @classmethod
    def normalize_name(
        cls,
        name: Optional[str]
    ) -> Optional[str]:
        """
        Normalizes person names.

        Example:
            "IRLA    GANGA siva SHANKAR"

                ↓

            "Irla Ganga Siva Shankar"
        """

        if not name:
            return None

        name = cls.clean(name)

        return name.title()

    # -----------------------------------------------------
    # Title Normalization
    # -----------------------------------------------------

    @classmethod
    def normalize_title(
        cls,
        title: Optional[str]
    ) -> Optional[str]:
        """
        Normalizes job titles.

        Example:

        "software engineer"

            ↓

        "Software Engineer"
        """

        if not title:
            return None

        title = cls.clean(title)

        return title.title()

    # -----------------------------------------------------
    # Paragraph Cleanup
    # -----------------------------------------------------

    @classmethod
    def normalize_paragraph(
        cls,
        text: Optional[str]
    ) -> Optional[str]:
        """
        Cleans multi-line text.

        Useful for resume summaries.
        """

        if not text:
            return None

        text = cls.clean(text)

        return text

    # -----------------------------------------------------
    # Remove Special Characters
    # -----------------------------------------------------

    @classmethod
    def remove_special_characters(
        cls,
        text: Optional[str]
    ) -> Optional[str]:
        """
        Removes unwanted symbols while preserving
        letters, numbers, spaces and common punctuation.
        """

        if not text:
            return None

        text = cls.clean(text)

        text = re.sub(
            r"[^A-Za-z0-9\s.,()/&+-]",
            "",
            text
        )

        return text

    # -----------------------------------------------------
    # Safe String
    # -----------------------------------------------------

    @staticmethod
    def safe_string(value) -> Optional[str]:
        """
        Safely converts any object to string.
        """

        if value is None:
            return None

        return str(value).strip()

    # -----------------------------------------------------
    # Empty Check
    # -----------------------------------------------------

    @staticmethod
    def is_empty(value) -> bool:
        """
        Returns True if value is empty.
        """

        if value is None:
            return True

        if isinstance(value, str):

            return value.strip() == ""

        return False

    # -----------------------------------------------------
    # Normalize Dictionary
    # -----------------------------------------------------

    @classmethod
    def normalize_candidate(
        cls,
        candidate: dict
    ) -> dict:
        """
        Applies text normalization to the candidate profile.
        """

        candidate["full_name"] = cls.normalize_name(
            candidate.get("full_name")
        )

        candidate["headline"] = cls.normalize_title(
            candidate.get("headline")
        )

        # Location

        location = candidate.get("location", {})

        location["city"] = cls.normalize_name(
            location.get("city")
        )

        location["region"] = cls.normalize_name(
            location.get("region")
        )

        location["country"] = cls.normalize_name(
            location.get("country")
        )

        candidate["location"] = location

        # Skills

        candidate["skills"] = [

            cls.clean(skill)

            for skill in candidate.get("skills", [])

            if cls.clean(skill)

        ]

        return candidate