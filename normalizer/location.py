"""
Location Normalizer

Normalizes city, region and country names.

"""

from __future__ import annotations

from typing import Optional

import pycountry


class LocationNormalizer:

    @staticmethod
    def normalize_country(
        country: Optional[str]
    ) -> Optional[str]:

        if not country:
            return None

        try:

            result = pycountry.countries.lookup(country)

            return result.alpha_2

        except LookupError:

            return country.title()

    @staticmethod
    def normalize_text(
        value: Optional[str]
    ) -> Optional[str]:

        if not value:
            return None

        return value.strip().title()

    @classmethod
    def normalize_candidate(
        cls,
        candidate: dict
    ) -> dict:

        location = candidate.get("location", {})

        location["city"] = cls.normalize_text(
            location.get("city")
        )

        location["region"] = cls.normalize_text(
            location.get("region")
        )

        location["country"] = cls.normalize_country(
            location.get("country")
        )

        candidate["location"] = location

        return candidate