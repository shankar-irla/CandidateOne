"""
Email Normalizer

Normalizes and validates email addresses used throughout the
CandidateOne pipeline.

Responsibilities
----------------
Remove whitespace
Convert to lowercase
Validate email format
Remove duplicates
Normalize candidate emails

"""

from __future__ import annotations

from typing import List, Optional

from email_validator import (
    validate_email,
    EmailNotValidError
)

class EmailNormalizer:
    """
    Email normalization utility.
    """

    # -----------------------------------------------------
    # Normalize Single Email
    # -----------------------------------------------------

    @staticmethod
    def normalize(
        email: Optional[str]
    ) -> Optional[str]:
        """
        Normalize a single email.

        Returns
        -------
        str | None
        """

        if not email:
            return None

        email = str(email).strip().lower()

        try:

            validated = validate_email(
                email,
                check_deliverability=False
            )

            return validated.normalized

        except EmailNotValidError:

            return None

    # -----------------------------------------------------
    # Normalize Email List
    # -----------------------------------------------------

    @classmethod
    def normalize_list(
        cls,
        emails: List[str]
    ) -> List[str]:
        """
        Normalizes a list of emails.
        """

        normalized = []

        seen = set()

        for email in emails:

            value = cls.normalize(email)

            if not value:
                continue

            if value in seen:
                continue

            seen.add(value)

            normalized.append(value)

        return normalized

    # -----------------------------------------------------
    # Candidate
    # -----------------------------------------------------

    @classmethod
    def normalize_candidate(
        cls,
        candidate: dict
    ) -> dict:
        """
        Normalizes candidate emails.
        """

        candidate["emails"] = cls.normalize_list(
            candidate.get("emails", [])
        )

        return candidate