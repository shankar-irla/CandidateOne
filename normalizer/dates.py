"""
Date Normalizer

Converts dates into YYYY-MM format.

"""

from __future__ import annotations

from typing import Optional

from dateutil.parser import parse


class DateNormalizer:

    @staticmethod
    def normalize(
        value: Optional[str]
    ) -> Optional[str]:

        if not value:
            return None

        try:

            dt = parse(str(value))

            return dt.strftime("%Y-%m")

        except Exception:

            return None

    @classmethod
    def normalize_experience(
        cls,
        experience: list
    ) -> list:

        for job in experience:

            if not isinstance(job, dict):
                continue

            job["start_date"] = cls.normalize(
                job.get("start_date")
            )

            job["end_date"] = cls.normalize(
                job.get("end_date")
            )

        return experience

    @classmethod
    def normalize_education(
        cls,
        education: list
    ) -> list:

        for record in education:

            if not isinstance(record, dict):
                continue

            record["start_date"] = cls.normalize(
                record.get("start_date")
            )

            record["end_date"] = cls.normalize(
                record.get("end_date")
            )

        return education

    @classmethod
    def normalize_candidate(
        cls,
        candidate: dict
    ) -> dict:

        candidate["experience"] = cls.normalize_experience(
            candidate.get("experience", [])
        )

        candidate["education"] = cls.normalize_education(
            candidate.get("education", [])
        )

        return candidate