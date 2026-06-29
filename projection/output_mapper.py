"""
Output Mapper

Maps the internal canonical candidate profile into a
target output schema using configurable field mappings.

Responsibilities
----------------
Map canonical fields
Apply default values
Handle nested objects
Flatten list values where appropriate
Produce projected profile

"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict

from projection.config_loader import ConfigLoader
from utils.logger import get_logger


class OutputMapper:
    """
    Maps canonical candidate profiles to configurable
    output schemas.
    """

    def __init__(
        self,
        config_loader: ConfigLoader
    ):

        self.logger = get_logger(__name__)

        self.config_loader = config_loader

        self.mapping = config_loader.get_mapping()

        self.defaults = config_loader.get_defaults()

    # ---------------------------------------------------------
    # Value Conversion
    # ---------------------------------------------------------

    @staticmethod
    def convert(value: Any) -> Any:
        """
        Converts canonical values into a serializable form.
        """

        if value is None:
            return None

        if isinstance(value, list):

            if len(value) == 0:
                return []

            # emails / phones → first value
            if all(isinstance(item, str) for item in value):

                return value[0] if len(value) == 1 else value

            return deepcopy(value)

        if isinstance(value, dict):

            return deepcopy(value)

        return value

    # ---------------------------------------------------------
    # Apply Defaults
    # ---------------------------------------------------------

    def apply_defaults(
        self,
        projected: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Adds default values where fields are missing.
        """

        for key, value in self.defaults.items():

            projected.setdefault(key, value)

        return projected

    # ---------------------------------------------------------
    # Projection
    # ---------------------------------------------------------

    def map_candidate(
        self,
        candidate: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Converts a canonical candidate into the target schema.
        """

        projected = {}

        for canonical_field, target_field in self.mapping.items():

            value = candidate.get(canonical_field)

            projected[target_field] = self.convert(value)

        projected = self.apply_defaults(projected)

        self.logger.info(
            "Projection completed successfully."
        )

        return projected

    # ---------------------------------------------------------
    # Multiple Candidates
    # ---------------------------------------------------------

    def map_candidates(
        self,
        candidates: list
    ) -> list:
        """
        Projects multiple candidates.
        """

        return [

            self.map_candidate(candidate)

            for candidate in candidates

        ]

    # ---------------------------------------------------------
    # Export Helper
    # ---------------------------------------------------------

    @staticmethod
    def to_dict(
        projected: Dict[str, Any]
    ) -> Dict[str, Any]:

        return deepcopy(projected)

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self):

        return (
            f"{self.__class__.__name__}"
            f"(mapped_fields={len(self.mapping)})"
        )