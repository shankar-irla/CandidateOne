"""
Phone Normalizer

Normalizes and validates phone numbers using the
phonenumbers library.

Responsibilities
----------------
Remove invalid phone numbers
Convert to E.164 format
Remove duplicates
Normalize candidate phone numbers

"""

from __future__ import annotations

from typing import List, Optional

import phonenumbers


class PhoneNormalizer:
    """
    Phone number normalization utility.
    """

    DEFAULT_REGION = "IN"

    # -----------------------------------------------------
    # Normalize Single Phone
    # -----------------------------------------------------

    @classmethod
    def normalize(
        cls,
        phone: Optional[str],
        region: str = DEFAULT_REGION
    ) -> Optional[str]:
        """
        Converts phone number to E.164 format.
        """

        if not phone:
            return None

        try:

            parsed = phonenumbers.parse(
                phone,
                region
            )

            if not phonenumbers.is_valid_number(parsed):
                return None

            return phonenumbers.format_number(
                parsed,
                phonenumbers.PhoneNumberFormat.E164
            )

        except Exception:

            return None

    # -----------------------------------------------------
    # Normalize List
    # -----------------------------------------------------

    @classmethod
    def normalize_list(
        cls,
        phones: List[str]
    ) -> List[str]:

        normalized = []

        seen = set()

        for phone in phones:

            value = cls.normalize(phone)

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

        candidate["phones"] = cls.normalize_list(
            candidate.get("phones", [])
        )

        return candidate