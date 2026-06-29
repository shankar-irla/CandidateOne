"""
Provenance Manager

Maintains field-level provenance information for every
candidate attribute.

Responsibilities
----------------
Track field origins
Track extraction methods
Merge provenance
Preserve explainability

"""

from __future__ import annotations

from copy import deepcopy
from typing import Dict, List


class ProvenanceManager:
    """
    Handles provenance generation and merging.
    """

    # ---------------------------------------------------------
    # Empty Provenance
    # ---------------------------------------------------------

    @staticmethod
    def empty() -> Dict:
        """
        Returns an empty provenance structure.
        """

        return {}

    # ---------------------------------------------------------
    # Add Field
    # ---------------------------------------------------------

    @staticmethod
    def add(
        provenance: Dict,
        field: str,
        source: str,
        method: str
    ) -> Dict:
        """
        Adds provenance information for a field.
        """

        provenance.setdefault(field, [])

        record = {
            "source": source,
            "method": method
        }

        if record not in provenance[field]:
            provenance[field].append(record)

        return provenance

    # ---------------------------------------------------------
    # Merge Provenance
    # ---------------------------------------------------------

    @classmethod
    def merge(
        cls,
        current: Dict,
        incoming: Dict
    ) -> Dict:
        """
        Merges two provenance dictionaries.
        """

        merged = deepcopy(current)

        for field, records in incoming.items():

            merged.setdefault(field, [])

            for record in records:

                if record not in merged[field]:

                    merged[field].append(record)

        return merged

    # ---------------------------------------------------------
    # Candidate
    # ---------------------------------------------------------

    @classmethod
    def merge_candidate(
        cls,
        current_candidate: Dict,
        incoming_candidate: Dict
    ) -> Dict:
        """
        Merges provenance from two candidates.
        """

        current = current_candidate.get(
            "provenance",
            {}
        )

        incoming = incoming_candidate.get(
            "provenance",
            {}
        )

        current_candidate["provenance"] = cls.merge(
            current,
            incoming
        )

        return current_candidate

    # ---------------------------------------------------------
    # Query
    # ---------------------------------------------------------

    @staticmethod
    def get_sources(
        provenance: Dict,
        field: str
    ) -> List[str]:
        """
        Returns unique sources for a field.
        """

        if field not in provenance:
            return []

        return sorted({

            record["source"]

            for record in provenance[field]

        })

    @staticmethod
    def get_methods(
        provenance: Dict,
        field: str
    ) -> List[str]:
        """
        Returns extraction methods used.
        """

        if field not in provenance:
            return []

        return sorted({

            record["method"]

            for record in provenance[field]

        })

    # ---------------------------------------------------------
    # Pretty Print
    # ---------------------------------------------------------

    @staticmethod
    def summarize(
        provenance: Dict
    ) -> Dict:
        """
        Returns simplified provenance summary.
        """

        summary = {}

        for field, records in provenance.items():

            summary[field] = [

                record["source"]

                for record in records

            ]

        return summary