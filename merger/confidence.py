"""
Confidence Calculator

Computes an overall confidence score for a merged
candidate profile.
"""

from __future__ import annotations

from typing import Dict, Any


class ConfidenceCalculator:
    """
    Computes confidence score for a canonical candidate.
    """

    # ---------------------------------------------------------
    # Source Reliability
    # ---------------------------------------------------------

    SOURCE_WEIGHTS = {
        "resume": 0.30,
        "linkedin": 0.25,
        "ats": 0.20,
        "github": 0.15,
        "recruiter_csv": 0.10
    }

    # ---------------------------------------------------------
    # Field Completeness
    # ---------------------------------------------------------

    FIELD_WEIGHTS = {
        "full_name": 0.08,
        "emails": 0.08,
        "phones": 0.08,
        "headline": 0.05,
        "skills": 0.10,
        "experience": 0.10,
        "education": 0.08,
        "location": 0.05,
        "links": 0.06
    }

    # ---------------------------------------------------------
    # Empty Check
    # ---------------------------------------------------------

    @staticmethod
    def is_present(value: Any) -> bool:
        """
        Returns True if a field contains meaningful data.
        """

        if value is None:
            return False

        if isinstance(value, str):
            return value.strip() != ""

        if isinstance(value, (list, tuple, set)):
            return len(value) > 0

        if isinstance(value, dict):
            return any(v not in (None, "", [], {}) for v in value.values())

        return True

    # ---------------------------------------------------------
    # Source Score
    # ---------------------------------------------------------

    @classmethod
    def source_score(
        cls,
        candidate: Dict
    ) -> float:
        """
        Calculates confidence contributed by data sources.

        Supports both formats:

        {
            "full_name": ["resume", "linkedin"]
        }

        and

        {
            "full_name": [
                {
                    "source": "resume"
                }
            ]
        }
        """

        provenance = candidate.get("provenance", {})

        discovered = set()

        if not isinstance(provenance, dict):
            return 0.0

        for records in provenance.values():

            if not isinstance(records, list):
                continue

            for record in records:

                if isinstance(record, str):

                    discovered.add(record)

                elif isinstance(record, dict):

                    source = record.get("source")

                    if source:
                        discovered.add(source)

        score = 0.0

        for source in discovered:

            score += cls.SOURCE_WEIGHTS.get(source, 0.0)

        return min(score, 0.60)

    # ---------------------------------------------------------
    # Completeness Score
    # ---------------------------------------------------------

    @classmethod
    def completeness_score(
        cls,
        candidate: Dict
    ) -> float:
        """
        Calculates confidence from populated fields.
        """

        score = 0.0

        for field, weight in cls.FIELD_WEIGHTS.items():

            if cls.is_present(candidate.get(field)):

                score += weight

        return min(score, 0.40)

    # ---------------------------------------------------------
    # Final Score
    # ---------------------------------------------------------

    @classmethod
    def calculate(
        cls,
        candidate: Dict
    ) -> float:
        """
        Returns overall confidence.
        """

        score = (
            cls.source_score(candidate)
            +
            cls.completeness_score(candidate)
        )

        return round(min(score, 1.0), 3)

    # ---------------------------------------------------------
    # Update Candidate
    # ---------------------------------------------------------

    @classmethod
    def update_candidate(
        cls,
        candidate: Dict
    ) -> Dict:
        """
        Updates candidate with calculated confidence.
        """

        candidate["overall_confidence"] = cls.calculate(candidate)

        return candidate