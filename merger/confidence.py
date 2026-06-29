"""
Confidence Calculator

Computes an overall confidence score for a merged
candidate profile.

Responsibilities
----------------
Source reliability scoring
Completeness scoring
Contact validation
Skills evaluation
Experience evaluation
Education evaluation
Profile completeness

"""

from __future__ import annotations

from typing import Dict


class ConfidenceCalculator:
    """
    Computes confidence score for a canonical candidate.
    """

    # ---------------------------------------------------------
    # Base Source Confidence
    # ---------------------------------------------------------

    SOURCE_WEIGHTS = {

        "resume": 0.30,

        "linkedin": 0.25,

        "ats": 0.20,

        "github": 0.15,

        "recruiter_csv": 0.10
    }

    # ---------------------------------------------------------
    # Completeness Weights
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
    def is_present(value) -> bool:

        if value is None:
            return False

        if isinstance(value, str):
            return value.strip() != ""

        if isinstance(value, (list, dict)):
            return len(value) > 0

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
        Calculates score based on contributing sources.
        """

        provenance = candidate.get(
            "provenance",
            {}
        )

        discovered = set()

        for records in provenance.values():

            for record in records:

                discovered.add(
                    record["source"]
                )

        score = 0.0

        for source in discovered:

            score += cls.SOURCE_WEIGHTS.get(
                source,
                0.0
            )

        return min(score, 0.60)

    # ---------------------------------------------------------
    # Completeness Score
    # ---------------------------------------------------------

    @classmethod
    def completeness_score(
        cls,
        candidate: Dict
    ) -> float:

        score = 0.0

        for field, weight in cls.FIELD_WEIGHTS.items():

            if cls.is_present(
                candidate.get(field)
            ):

                score += weight

        return min(score, 0.40)

    # ---------------------------------------------------------
    # Overall
    # ---------------------------------------------------------

    @classmethod
    def calculate(
        cls,
        candidate: Dict
    ) -> float:
        """
        Computes final confidence score.
        """

        score = (

            cls.source_score(candidate)

            +

            cls.completeness_score(candidate)

        )

        return round(

            min(score, 1.0),

            3

        )

    # ---------------------------------------------------------
    # Candidate
    # ---------------------------------------------------------

    @classmethod
    def update_candidate(
        cls,
        candidate: Dict
    ) -> Dict:

        candidate["overall_confidence"] = (

            cls.calculate(candidate)

        )

        return candidate