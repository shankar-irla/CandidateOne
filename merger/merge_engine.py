"""
Merge Engine

Orchestrates the complete candidate merge process.

Responsibilities
----------------
Merge candidate profiles
Resolve conflicts
Merge provenance
Compute confidence
Produce a single canonical profile

"""

from __future__ import annotations

from copy import deepcopy
from typing import Dict, List

from merger.conflict_resolver import ConflictResolver
from merger.provenance import ProvenanceManager
from merger.confidence import ConfidenceCalculator
from models.canonical_schema import empty_candidate
from utils.logger import get_logger


class MergeEngine:
    """
    Merge engine for CandidateOne.
    """

    def __init__(self):

        self.logger = get_logger(__name__)

    # ---------------------------------------------------------
    # Merge Two Candidates
    # ---------------------------------------------------------

    def merge_two(
        self,
        current: Dict,
        incoming: Dict,
        current_source: str,
        incoming_source: str
    ) -> Dict:
        """
        Merges two candidate profiles.
        """

        self.logger.info(
            "Merging %s -> %s",
            current_source,
            incoming_source
        )

        merged = ConflictResolver.merge_candidate(
            current,
            incoming,
            current_source,
            incoming_source
        )

        merged = ProvenanceManager.merge_candidate(
            merged,
            incoming
        )

        return merged

    # ---------------------------------------------------------
    # Merge Multiple Candidates
    # ---------------------------------------------------------

    def merge(
        self,
        candidates: List[Dict]
    ) -> Dict:
        """
        Merge multiple candidate profiles into
        one canonical profile.
        """

        if not candidates:

            return empty_candidate()

        merged = deepcopy(candidates[0])

        current_source = self.detect_source(
            merged
        )

        for candidate in candidates[1:]:

            incoming_source = self.detect_source(
                candidate
            )

            merged = self.merge_two(
                merged,
                candidate,
                current_source,
                incoming_source
            )

        merged = ConfidenceCalculator.update_candidate(
            merged
        )

        self.logger.info(
            "Candidate merge completed."
        )

        return merged

    # ---------------------------------------------------------
    # Detect Source
    # ---------------------------------------------------------

    @staticmethod
    def detect_source(
        candidate: Dict
    ) -> str:
        """
        Determines the originating source.

        Falls back to 'unknown'.
        """

        provenance = candidate.get(
            "provenance",
            {}
        )

        if not provenance:
            return "unknown"

        for records in provenance.values():

            if records:

                record = records[0]

                if isinstance(record, dict):

                    return record.get(
                        "source",
                        "unknown"
                    )

        return "unknown"

    # ---------------------------------------------------------
    # Merge Convenience
    # ---------------------------------------------------------

    @classmethod
    def merge_profiles(
        cls,
        *profiles: Dict
    ) -> Dict:
        """
        Convenience method.

        Example
        -------
        MergeEngine.merge_profiles(
            resume,
            linkedin,
            github
        )
        """

        engine = cls()

        profiles = [

            profile

            for profile in profiles

            if profile

        ]

        return engine.merge(
            profiles
        )